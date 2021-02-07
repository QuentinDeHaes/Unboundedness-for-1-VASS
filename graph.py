from Node import *
from helper_functions import *
from Closure import *
from copy import copy, deepcopy


class Graph:
    def __init__(self, start_node: Node):
        """
        initialise the Graph with the counter (z_value) on 0 and the start_node specified
        along with a list of all nodes within the graph
        :param start_node:
        """
        self.start_node = start_node
        self.current_node = start_node
        self.z_value = 0
        self.nodes = {start_node}

    def add_node(self, node: Node):
        """
        add a node to the list of nodes
        :param node:
        :return:
        """
        self.nodes.add(node)

    def get_nodes(self):
        """
        returns a list of all nodes in the graph
        :return:
        """
        return self.nodes

    def set_nodes(self, nodes):
        """
        set the list of nodes of the graph to nodes
        :param nodes:
        :return:
        """
        self.nodes = set(nodes)

    def __copy__(self):
        """
        create a new copy of the current graph
        :return: copy (Graph)
        """
        cop = Graph(self.start_node.__copy__())
        cop.current_node = self.current_node.__copy__()
        cop.z_value = self.z_value
        cop.nodes = deepcopy(self.nodes)
        if hasattr(self, "cycles"):
            cop.cycles = deepcopy(self.cycles)
        return cop

    def to_dot(self, filename):
        """
        make a visual representation of the graph
        :param filename: the file in which the dot-code needs to be put
        :return: Node
        """
        f = open(filename, "w")

        # do a BFS over the graph to find everything (that is connected to start_node)
        already_added = {self.start_node}
        already_visited = set()
        to_visit = [self.start_node]

        f.write("digraph G {\n")
        f.write("  " + self.start_node.dot_value() + '\n')
        while len(to_visit) != 0:
            current = to_visit[0]
            to_visit = to_visit[1:]
            already_visited.add(current)

            for node, amount in current.get_edges():
                if node not in already_added:
                    already_added.add(node)
                    f.write("  " + node.dot_value() + '\n')
                f.write("    s{} -> s{} [label = {}]\n".format(current.id, node.id, amount))
                if node not in already_visited:
                    to_visit.append(node)

        f.write("}\n")

        f.close()

    def reset_distances(self):
        """
        reset all distances to infinity so bellman ford can be rerun
        :return:
        """
        for node in self.nodes:
            node.distance = math.inf

    def bellman_ford_alg(self):
        """
        execute the bellman ford algorithm to get shortest path of nodes (will be used as base to find positive cycles
        :return:
        """
        self.start_node.distance = 0
        # bellman ford needs V-1 iterations to certainly have shortest path (without negative cycles)
        for i in range(len(self.nodes) - 1):
            # by going over all nodes and their outgoing edges, we go over all edges
            for node in self.nodes:
                for edge in node.edges:
                    edge[0].update_distance(node.distance + edge[1])

    def get_cycles(self):
        """
        we use bellman ford to find cycles, because we need positive cycles and it finds negative ones we simply negate
        all values on edges
        :return: a list of all nodes in cycles and their incrementation
        - the initial bellman part is O(VE)
        - the next part is only a single bellman run so O(E)
        - and the final part is V-1 times O(V³E) so in total O(V⁴E)
        """
        # TODO check possible issue with node being in 2 different cycles
        # TODO possible issue with 2 cycles sharing nodes splitting and coming back with where
        #  split has identical weight but different amount of nodes: can be fixed by making every cycle and
        #  prospective cycle run 1 by one in (and update 1 by 1) but this will end in far less efficiency still
        #

        self.start_node.distance = 0
        self.cycles = dict()
        # bellman ford needs V-1 iterations to certainly have shortest path (without negative cycles)
        for i in range(len(self.nodes) - 1):
            # by going over all nodes and their outgoing edges, we go over all edges
            for node in self.nodes:
                for edge in node.edges:
                    edge[0].update_distance(node.distance - edge[1])
        # with this, we have done the regular bellman ford with negated values
        # now we will check for more changes
        edges_in_cycles = set()
        possible_cycles = set()
        complete_cycles = set()
        # we test whether a (positive) cycle actually exists, this takes E time
        change = False
        # by going over all nodes and their outgoing edges, we go over all edges
        for node in self.nodes:
            for edge in node.edges:
                # if ,after already doing entire bellman ford, there still is a change in the distance,
                # there exists a negative cycle, we will add this new node to the list
                if edge[0].distance > node.distance - edge[1]:
                    change = True
                    # add the update-able nodes and their incoming edge in a list to update after this run
                    # over all edges
                    edges_in_cycles.add((node, edge[0], edge[1]))

                    if node.id == edge[0].id:
                        # if the node has an edge to itself, it is in a cycle with only itself
                        complete_cycles.add(((node, node), edge[1]))
                        self.cycles[((node, node), edge[1])] = len(complete_cycles)
                    else:
                        # otherwise it is possibly a cycle with others,
                        # so we set the current path and the amount it is currently increased with
                        possible_cycles.add(((node, edge[0]), edge[1]))

        # if nothing changed there are no positive cycles and we can quit
        if not change:
            return set()

        # now that we're here, we know a (positive) cycle actually exists
        # the largest cycle will (in worst case ) have every node in the cycle, so we'll need to check for V times
        # to ensure we have checked for every cycle, since we've already done it once to ensure we have cycles we'll do
        # it V-1 times more
        for i in range(len(self.nodes) - 1):

            # update distances from previous run
            # O(E)
            for edge in edges_in_cycles:
                edge[1].update_distance(edge[0].distance - edge[2])
            edges_in_cycles = set()

            # O(E)
            for node in self.nodes:
                for edge in node.edges:
                    # if ,after already doing entire bellman ford, there still is a change in the distance,
                    # there exists a negative cycle, we will add this new node to the list
                    if edge[0].distance > node.distance - edge[1]:
                        edges_in_cycles.add((node, edge[0], edge[1]))

            # we check whether the edge can be added to our prospective cycles
            new_possible_cycles = set()
            for edge in edges_in_cycles:
                # every edge can only be in here once at a time, making this O(E)
                for cycle in possible_cycles:
                    # because we know the maximum size of a cycle is V and the way this is constructed
                    # and possible_cycles can only have V! entries, which falls under O(V²)
                    # making these for-loops O(EV³)
                    if edge[0] == cycle[0][-1]:
                        # if the newest node is our first node, the cycle is complete
                        if cycle[0][0] == edge[1]:
                            # the cycle is complete so we add it to complete_cycles
                            complete_cycles.add((cycle[0] + (edge[1],), cycle[1] + edge[2]))
                            self.cycles[(cycle[0] + (edge[1],), cycle[1] + edge[2])] = len(complete_cycles)
                        elif edge[1] not in cycle[0]:
                            # the cycle isn't finished so we add it to the new possible cycles,
                            # if a subsidiary cycle is found, that cycle will also be found elsewhere
                            # and we no longer need this part
                            new_possible_cycles.add((cycle[0] + (edge[1],), cycle[1] + edge[2]))

            possible_cycles = new_possible_cycles

        return complete_cycles

    def set_non_allowable_values(self, complete_cycles):
        """
        set on each node on which values, the cycle can't be taken
        :param complete_cycles: the cycles as received by the get_cycles method
        :return:None (the changes happen on the node-classes)
        this code is O(V⁴)
        """
        # per cycle we run this code (at most O(V²))
        for cycle in complete_cycles:

            # distances is O(V*E)
            distances = get_distances_in_path(cycle[0])

            # for each node in the cycle we run this the code (this loop  is O(V))
            for node_i in range(len(cycle[0]) - 1):
                not_allowed = []
                current_add = 0
                minimal_add = 0

                not_allowed += [num - cycle[1] for num in cycle[0][:-1][node_i].get_disequalities()]
                current_add += distances[node_i % (len(cycle[0]) - 1)]
                if current_add < minimal_add:
                    minimal_add = current_add

                # we run over every edge in the cycle (also O(V))
                for j in range(1, len(distances)):
                    not_allowed += [num - current_add for num in
                                    cycle[0][:-1][(node_i + j) % (len(cycle[0]) - 1)].get_disequalities()]

                    current_add += distances[(node_i + j) % (len(cycle[0]) - 1)]
                    if current_add < minimal_add:
                        minimal_add = current_add

                if not hasattr(cycle[0][node_i], 'non_cyclables'):
                    cycle[0][node_i].non_cyclables = dict()
                    cycle[0][node_i].minimal_cyclable = dict()

                cycle[0][node_i].non_cyclables[self.cycles[cycle]] = not_allowed
                cycle[0][node_i].minimal_cyclable[self.cycles[cycle]] = -minimal_add

    def DEPRECATED_get_bounded_chains_DEPRECATED(self, complete_cycles):
        """
        DEPRECATED
        for our algorithm, we need U₀, which is the unbounded chains from the positive cycles, they are unbounded,
        thus they can't be represented that easily, but the complement, the bounded chains can.
        :param complete_cycles: the cycles as received by the get_cycles method
        :return: None (the changes happen on the node-classes)
        O(V⁴*X) with X being linear, but based on the size of the disequality

        DEPRECATED
        """
        # DEPRECATED
        # O(V²) to run over all cycles
        for cycle in complete_cycles:
            # O(V) to run over an entire cycle
            for node_i in range(len(cycle[0]) - 1):

                if not hasattr(cycle[0][node_i], 'bounded_chains'):
                    cycle[0][node_i].bounded_chains = dict()

                bounded_chains = []
                non_cyclables = cycle[0][node_i].non_cyclables[self.cycles[cycle]]
                minimal_cyclable = cycle[0][node_i].minimal_cyclable[self.cycles[cycle]]
                positive_cycle_value = cycle[1]

                # O(V) as long as we assume that the maximum amount of disequalities a node can have is fixed
                non_cyclables = cleanup_non_cyclables(non_cyclables, positive_cycle_value, minimal_cyclable)
                # O(V) as long as we assume that the maximum amount of disequalities a node can have is fixed
                for key in non_cyclables:
                    value = int(minimal_cyclable / positive_cycle_value) * positive_cycle_value + key
                    # O(X) this is linear, but based on the size of the disequality
                    # (and based on the amount a cycle increments the countervalue with)
                    while value <= non_cyclables[key]:
                        bounded_chains.append(value)
                        value += positive_cycle_value

                cycle[0][node_i].bounded_chains[self.cycles[cycle]] = bounded_chains

    #    DEPRECATED

    def get_unbounded_chains(self, complete_cycles):
        """
        for our algorithm, we need U₀, which is the unbounded chains from the positive cycles, they are unbounded,
        thus they will be represented using upward closures, we only need the chains above the disequalities
         (the amount of disequalties is bounded by O(V), so the amount of chains we need is also bounded by O(V)
        :param complete_cycles: the cycles as received by the get_cycles method
        :return: None (the changes happen within the graph)
        O(V⁴)

        """
        self.U0 = set()
        # O(V²) to run over all cycles
        for cycle in complete_cycles:
            # O(V) to run over an entire cycle
            for node_i in range(len(cycle[0]) - 1):

                non_cyclables = cycle[0][node_i].non_cyclables[self.cycles[cycle]]
                minimal_cyclable = cycle[0][node_i].minimal_cyclable[self.cycles[cycle]]
                positive_cycle_value = cycle[1]
                # O(V) as long as we assume that the maximum amount of disequalities a node can have is fixed
                non_cyclables = cleanup_non_cyclables(non_cyclables, positive_cycle_value, minimal_cyclable)
                # O(V) as each node can have as many non_cyclables as disequalities in the cycle (which is bounded by nodes)
                for non_cyc in non_cyclables:
                    self.U0.add((cycle[0][node_i],
                                 Closure(non_cyclables[non_cyc] + positive_cycle_value, None, positive_cycle_value)))

    def get_bounded_chains(self, complete_cycles):
        """
        in order to continue our algorithm, we need the bounded chains, so we'll calculate them
        O(V⁴)
        """
        # TODO remove the singularization of closures in the same thingie, make it 2 different closures
        #  from A to B and from B to C instead of A to C
        bounded_chains = dict(set())
        # O(V²) to run over all cycles
        for cycle in complete_cycles:
            # O(V) to run over an entire cycle
            for node_i in range(len(cycle[0]) - 1):

                non_cyclables = cycle[0][node_i].non_cyclables[self.cycles[cycle]]
                minimal_cyclable = cycle[0][node_i].minimal_cyclable[self.cycles[cycle]]
                positive_cycle_value = cycle[1]

                # O(V²) as long as we assume that the maximum amount of disequalities a node can have is fixed
                non_cyclables = cleanup_non_cyclables(non_cyclables, positive_cycle_value, minimal_cyclable)
                # O(V) as long as we assume that the maximum amount of disequalities a node can have is fixed
                for key in non_cyclables:
                    value = int(minimal_cyclable / positive_cycle_value) * positive_cycle_value + key
                    if node_i not in bounded_chains:
                        bounded_chains[node_i] = set()  # create the bounded chains of the node if they do not yet exist
                    non_cyclables[key].insert(0, value)

                    for i in range(len(non_cyclables[key]) - 1):  # create all closure used for the chain

                        bounded_chains[node_i].add(
                            Closure(non_cyclables[key][i], non_cyclables[key][i + 1], positive_cycle_value))

        return bounded_chains

    def top(self):
        """
        calculate the top(Q) of the graph, this is simply a calculation of the amount of values we need to test from each top of a bounded chain.
        defined by proposition 5 of the paper :Coverability in Succinct One-Counter Nets with Disequality Tests
        and lemma 4 used to calculate p(Q) and poly_2
        :return: top(Q)
        this is constant efficiëncy O(1)
        """
        Q = len(self.nodes)
        poly2Q = (Q * Q + 2) * (Q + 1) + 1
        P_Q = (2 * Q * Q) * (Q * Q + 2) * (Q + 1) + Q * (2 * Q + 1) * poly2Q
        top = 2 * Q * Q * P_Q
        return top

    def BoundedCoverWithObstacles_GetL(self):
        """
        the polynomial function that returns the maximal length a bounded coverability with obstacles should take, defined by proposition 7 of the paper
        Coverability in Succinct One-Counter Nets with Disequality Tests provided to me by professor perez
        :return: L
        """
        Q = len(self.nodes)

        T = self.top()
        poly1 = Q * Q + Q + 3 + Q * T
        L = Q * pow(poly1, 2) + Q * Q + 3
        return L

    def _getAllReachable1Step(self, original_nodes):
        reachable = set()
        for node in original_nodes:
            lis= node[0].get_edges()
            for new_node in lis:
                if node[1]+new_node[1] not in new_node[0].get_disequalities():
                    reachable.add((new_node[0], node[1]+new_node[1]))


        return reachable

    def getBoundedCoverWithObstacles(self, cycles):
        return

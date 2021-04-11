from Node import *
from helper_functions import *
from Closure import *
from copy import copy, deepcopy
from Un_representation import Un, O_equationset

import Bounded_coverability_with_obstacles


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
        if hasattr(self, 'nodes_in_cycles'):
            cop.nodes_in_cycles = deepcopy(self.nodes_in_cycles)
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

    def get_cycles_OLD(self):
        """
        DEPRECATED
        we use bellman ford to find cycles, because we need positive cycles and it finds negative ones we simply negate
        all values on edges
        :return: a list of all nodes in cycles and their incrementation
        - the initial bellman part is O(VE)
        - the next part is only a single bellman run so O(E)
        - and the final part is V-1 times O(V³E) so in total O(V⁴E)
        """
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

    def get_cycles(self):
        """
        locate all cycles necessary for our algorithm, for each node in a positive cycle, it's optimal positive cycle (for each the one with the highest pmin value)
        :return:  a set of all nodes in cycles and their incrementation
        """
        self.cycles = dict()
        max_weight = 0
        for node in self.nodes:
            for edge in node.get_edges():
                max_weight = max(abs(edge[1]), max_weight)

        cycle_set = set()
        self.nodes_in_cycles = []
        for node in self.nodes:
            cycle = self.get_cycle_singleNode(node, max_weight)
            if cycle[2] != -1:
                self.nodes_in_cycles.append(node)
                add_to_list = True
                for old_cycle in cycle_set:
                    if old_cycle[1] == cycle[2] and (set(old_cycle[0]) == set(cycle[1])):
                        add_to_list = False
                        break
                if add_to_list:
                    cycle_set.add((tuple(cycle[1]), cycle[2]))
        cycle_set2 = list(cycle_set)
        for i in range(len(cycle_set2)):
            self.cycles[cycle_set2[i]] = i
        return cycle_set

    def get_cycle_singleNode(self, node, maxWeight):
        """
        get the optimal positive cycle (highest pmin) for a given node if one exists
        :param node: the node for which we search the optimal cycle
        :param maxWeight: the highest absolute value of weight any edge in the graph possesses
        :return: 3pair of optimal pmin, the cycle and the weight of the cycle
        """

        maxval = 0
        minval = -len(self.nodes) * maxWeight
        res = 0, [], -1
        while minval <= maxval:
            test_val = (maxval + minval) // 2
            result = self._locate_cycle_dfs([node], test_val, 0)
            if result[0]:
                res = test_val, result[1], result[2]
                new_minval = test_val
                new_maxval = maxval
            else:
                new_minval = minval
                new_maxval = test_val
            if new_minval == minval and new_maxval == maxval:  # fixing a bug where it stays stuck due to integerdivision
                # because we do need to try if they're equal at least once, due to minval theoretically possibly starting at 0
                break
            else:
                minval = new_minval
                maxval = new_maxval

        return res

    def _locate_cycle_dfs(self, current_path, min_score, current_score):
        """
        the recursive function to acquire a positive cycle with a pmin higher than (or equal to minscore)
        :param current_path: a list of all nodes we have already visited
        :param min_score: the current minimal score, if we go below, we need to try another path
        :param current_score: the current score of our cycle
        :return: successbool, complete_cycle (if succesful else []), weight of the cycle (if succesfull else -1)
        """

        if current_path[0] == current_path[-1] and len(current_path) > 1:
            if current_score > 0:
                return True, current_path, current_score
            else:  # we have located a negative cycle (with a score higher than minscore)
                return False, [], -1

        for node, w in current_path[-1].edges:
            if current_score + w >= min_score and node not in current_path[1:]:
                value = self._locate_cycle_dfs(current_path + [node], min_score, current_score + w)
                if value[0]:
                    return value
        return False, [], -1

    def _locate_cycle_bellman(self, current_path, min_score, current_score):
        """
        the cycle_location method using bellman ford, made as place in replacement to the _locate_cycle_df
        method
        :param current_path: a list of all nodes we have already visited
        :param min_score: the current minimal score, if we go below, we need to try another path
        :param current_score: the current score of our cycle
        :return: successbool, complete_cycle (if succesful else []), weight of the cycle (if succesfull else -1)
        """
        self.reset_distances()
        # start by setting up bellman so no infinities remain (if everything is reachable)
        self.bellman_ford_alg()
        edges_in_cycles = set()
        starter_node = current_path[0]
        success = False
        for i in range(len(self.nodes) - 1):
            # update distances from previous run
            # O(E)
            for edge in edges_in_cycles:
                edge[1].update_distance(edge[0].distance - edge[2])
            edges_in_cycles = set()

            for node in self.nodes:
                for edge in node.edges:
                    # if ,after already doing entire bellman ford, there still is a change in the distance,
                    # there exists a negative cycle, we will add this new node to the list
                    if edge[0].distance > node.distance - edge[1]:
                        edges_in_cycles.add((node, edge[0], edge[1]))
                        # keep updating the graph until our starternode is the one that will be updating new nodes using it's edges
                        if node == starter_node:
                            success = True
                            break
                if success:
                    break
            if success:
                break

        if success:
            possible_cycles = {((starter_node,), current_score)}
            found_nodes = {starter_node}
            for i in range(len(self.nodes) - 1):

                edges_in_cycles = set()
                for node in found_nodes:
                    for edge in node.edges:
                        # if ,after already doing entire bellman ford, there still is a change in the distance,
                        # there exists a negative cycle, we will add this new node to the list
                        if edge[0].distance > node.distance - edge[1]:
                            edges_in_cycles.add((node, edge[0], edge[1]))
                new_possible_cycles = set()
                found_nodes = set()

                for edge in edges_in_cycles:
                    # every edge can only be in here once at a time, making this O(E)
                    for cycle in possible_cycles:
                        # because we know the maximum size of a cycle is V and the way this is constructed
                        # and possible_cycles can only have V! entries, which falls under O(V²)
                        # making these for-loops O(EV³)
                        if edge[0] == cycle[0][-1]:
                            # if the newest node is our first node, the cycle is complete
                            if cycle[0][0] == edge[1]and cycle[1] + edge[2] > min_score:
                                # the cycle is complete so we add it to complete_cycles
                                return True, cycle[0]+(edge[1],), cycle[1] + edge[2]
                            elif edge[1] not in cycle[0] and cycle[1] + edge[2] > min_score:
                                # the cycle isn't finished so we add it to the new possible cycles,
                                # if a subsidiary cycle is found, that cycle will also be found elsewhere
                                # and we no longer need this part

                                new_possible_cycles.add((cycle[0] + (edge[1],), cycle[1] + edge[2]))
                                found_nodes.add(edge[1])
                possible_cycles = new_possible_cycles
                for edge in edges_in_cycles:
                    edge[1].update_distance(edge[0].distance - edge[2])

        return False, [], -1


    def set_non_allowable_values(self, complete_cycles):
        """
        set on each node on which values, the optimal cycle can't be taken
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
                    cycle[0][node_i].non_cyclables = []
                    cycle[0][node_i].minimal_cyclable = float("inf")

                if cycle[0][node_i].minimal_cyclable > -minimal_add:
                    cycle[0][node_i].non_cyclables = not_allowed
                    cycle[0][node_i].minimal_cyclable = -minimal_add
                    cycle[0][node_i].optimal_cycle = cycle

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

    def get_unbounded_chains(self):
        """
        for our algorithm, we need U₀, which is the unbounded chains from the positive cycles, they are unbounded,
        thus they will be represented using upward closures, we only need the chains above the disequalities
         (the amount of disequalties is bounded by O(V), so the amount of chains we need is also bounded by O(V)
        :return: None (the changes happen within the graph)
        O(V⁴)

        """
        self.U0 = list()
        for node in self.nodes_in_cycles:
            optimal_cycle = node.optimal_cycle
            non_cyclables = node.non_cyclables
            minimal_cyclable = node.minimal_cyclable
            positive_cycle_value = optimal_cycle[1]
            # O(V) as long as we assume that the maximum amount of disequalities a node can have is fixed
            non_cyclables = chain_max_non_cyclables(non_cyclables, positive_cycle_value, minimal_cyclable)
            # O(V) as each node can have as many non_cyclables as disequalities in the cycle (which is bounded by nodes)
            for non_cyc in non_cyclables:
                self.U0.append((node,
                                Closure(non_cyclables[non_cyc] + positive_cycle_value, None, positive_cycle_value)))

    def get_bounded_chains(self):
        """
        in order to continue our algorithm, we need the bounded chains, so we'll calculate them
        O(V⁴)
        """
        bounded_chains = dict(list())
        # O(V²) to run over all cycles
        for node in self.nodes_in_cycles:
            optimal_cycle = node.optimal_cycle
            non_cyclables = node.non_cyclables
            minimal_cyclable = node.minimal_cyclable
            positive_cycle_value = optimal_cycle[1]

            # O(V²) as long as we assume that the maximum amount of disequalities a node can have is fixed
            non_cyclables = cleanup_non_cyclables(non_cyclables, positive_cycle_value, minimal_cyclable)
            # O(V) as long as we assume that the maximum amount of disequalities a node can have is fixed
            for key in non_cyclables:
                value = int(minimal_cyclable / positive_cycle_value) * positive_cycle_value + key
                if node not in bounded_chains:
                    bounded_chains[
                        node] = list()  # create the bounded chains of the node if they do not yet exist
                non_cyclables[key].insert(0, value)

                for i in range(len(non_cyclables[key]) - 1):  # create all closure used for the chain

                    bounded_chains[node].append(
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
        # TODO improve 200
        return 200
        Q = len(self.nodes)
        poly2Q = (Q * Q + 2) * (Q + 1) + 1
        P_Q = (2 * Q * Q) * (Q * Q + 2) * (Q + 1) + Q * (2 * Q + 1) * poly2Q
        top = (2 * Q * Q) * P_Q
        return top

    def BoundedCoverWithObstacles_GetL(self):
        """
        the polynomial function that returns the maximal length a bounded coverability with obstacles should take, defined by proposition 7 of the paper
        Coverability in Succinct One-Counter Nets with Disequality Tests provided to me by professor perez
        :return: L
        """
        # TODO improve 1000
        return 1000
        Q = len(self.nodes)

        T = self.top()
        poly1 = (Q * Q) + Q + 3 + (Q * T)
        L = Q * pow(poly1, 2) + Q * Q + 3
        return L

    def bndCoverWObstacles(self, cycles, chains):
        """
        the method used to acquire the non-trivial unbounded values
        :param cycles: the list of all cycles
        :param chains: the list of bounded chains
        :return: the bounded chains after removing the non-trivial unbounded values, i.e the complement of U0
        """
        self.U_n = Un(self, chains)  # generate U_0
        top = self.top()  # get the value Top a polynomial based on the amount of nodes
        change = True
        n = 0
        L = self.BoundedCoverWithObstacles_GetL()  # get the value L a polynomial based on the amount of nodes
        while change:  # run until U_n-1 == U_n
            change = False
            to_delete = set()
            for node in chains:  # check every node in the positive cycles (all bounded chains)

                for chain in chains[node]:  # check all bounded chains linked to the given node
                    for i in range(min(top,
                                       chain.len())):  # check the highest top values in the chain to see whether it can reach current U_n (starting from the highest)
                        can_reach = False
                        for o_i in self.U_n.list_O_i():  # check whether it can reach any O_i in U_n
                            value = chain[chain.len() - i - 1]
                            can_reach = Bounded_coverability_with_obstacles.Bounded_coverability_with_obstacles(
                                (node, value), o_i[0], L, o_i[1])
                            if can_reach:

                                new_minval = chain.minVal

                                change = True
                                if i == 0:
                                    # remove the chain completely as all values in it are now unbounded
                                    chains[node].remove(chain)
                                    if len(chains[node]) == 0:
                                        to_delete.add(node)
                                else:  # reduce the  chain to only the top values that cannot reach U_n (as all below the one that can reach U_n can simply take the cycle some times)
                                    chain.minVal = chain[chain.len() - (i - 1) - 1]
                                # edit U_n to to add the new values
                                self.U_n.edit_non_triv_q_residueclass(node, chain.step, chain.minVal % chain.step,
                                                                      new_minval, chains[node])
                                break
                        if can_reach:
                            break
            for node in to_delete:
                del chains[node]
            n += 1

        return chains, n

    def coverable(self, source, L):
        """
        check whether a source can reach our current version(normally final version if used at proper time) of U_n
        :param source:the source
        :param L: the polynomial value L given to many functions gotten from g.BoundedCoverWithObstacles_GetL()
        :return: bool :is it coverable?
        """
        for o_i in self.U_n.list_O_i():  # check for every O_i in U_n if source can reach itl
            result = Bounded_coverability_with_obstacles.Bounded_coverability_with_obstacles(
                source, o_i[0], L, o_i[1])

            if result:
                return True
        return False

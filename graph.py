from Node import *
from helper_functions import *
from Closure import *
from copy import copy, deepcopy
from Un_representation import Un, O_equationset
from CONFIG import CONFIG

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
            result = self._locate_cycle_bellman([node], test_val, 0)
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

    def _locate_cycle_bellman(self, current_path, min_score, current_score=0, goal_node=None):
        """
                the cycle_location method using bellman ford in a polynomial manner,
                made as place in replacement to the _locate_cycle_df method
                :param current_path: a list of all nodes we have already visited, initially set to our single starternode
                :param min_score: the current minimal score, if we go below, we need to try another path
                :param current_score: the current score of our cycle
                :param goal_node: the node we are trying to reach, if None, it will be set to the starternode in currentpath
                :return: successbool, complete_cycle (if succesful else []), weight of the cycle (if succesfull else -1)
                """
        self.reset_distances()
        self._reset_pmins()
        # start by setting up bellman so no infinities remain (if everything is reachable)
        self.bellman_ford_alg()
        original_current_score = current_score
        edges_in_cycles = set()
        starter_node = current_path[0]
        if goal_node is None:
            goal_node = starter_node
        success = False
        for i in range(len(self.nodes)):
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
            starter_node.pminval = ([], current_score)

            found_nodes = {starter_node}

            for i in range(len(self.nodes)):

                edges_in_cycles = set()
                for node in found_nodes:
                    for edge in node.edges:
                        # if ,after already doing entire bellman ford, there still is a change in the distance,
                        # there exists a positive cycle, we will add this new node to the list
                        if edge[0].distance > node.distance - edge[1] and node.pminval[1] + edge[1] >= min_score and edge[0] not in node.pminval[0][1:]:
                            edges_in_cycles.add((node, edge[0], edge[1]))
                found_nodes = set()

                for edge in edges_in_cycles:
                    # every edge can only be in here once at a time, making this O(E)
                    if edge[1].pminval[1] < edge[0].pminval[1] + edge[2]:
                        # update the node and pminvalue etc only if it is actually an improvement to before
                        edge[1].update_distance(edge[0].distance - edge[2])
                        edge[1].pminval = (edge[0].pminval[0]+[edge[0]], edge[0].pminval[1] + edge[2])
                        found_nodes.add(edge[1])
                if goal_node.pminval[0] != []:
                    return True, goal_node.pminval[0]+[goal_node], goal_node.pminval[1]
                    # we have located a cycle that does not violate our current minimal pmin, so now we'll generate the
                    # cycle from back to forward by checking from where the update of the previous node came, checking
                    # where the update of that node came from, until we reach the starternode once more
                    # O(V) due to it not being a cycle otherwise

                    cycle = [goal_node]
                    current_node = goal_node.pminval[0]
                    while current_node != starter_node:
                        if current_node not in cycle:
                            cycle.append(current_node)
                            current_node = current_node.pminval[0]
                        else:
                            # it is possible that another (smaller in node amount) positive cycle has
                            # embedded itself into our solution, where we can't go backward anymore, because we'd
                            # continuously update the new cycle and thus create an infinite cycle within our cycle,
                            # since this is not something we want, we'd want to back in time to the point where
                            # pminval did not yet have this internal cycle there,
                            # and while we can't turn back time, we can just rerun part of the algorithm until we reach
                            # the point where the internal cycle does not yet exist, but we still have reached the wanted node,
                            # which is the first node we noticed in the cycle.
                            # we cannot redo the algorithm an infinite amount of times, since that wouldn't be polynomial.
                            # Luckily, we don't have to, since this can only really occur once for each node in the cycle (except the starternode)
                            # sw we need to rerun (part of) the algorithm at most O(V) times
                            cycle = cycle[:cycle.index(current_node)]
                            val = self._locate_cycle_bellman([starter_node], min_score, original_current_score,
                                                             current_node)
                            val[1].reverse()
                            cycle += val[1][:-1]
                            current_node = val[1][-1]
                    cycle.append(starter_node)
                    cycle.reverse()
                    score = sum(list(get_distances_in_path(cycle)))
                    if score > 0:
                        return True, cycle, score
                    else:
                        return False, cycle, -1

        return False, [], -1

    def _reset_pmins(self):
        """
        a subsidiary function for the bellman-ford alteration of locating cycles that will reset
        a variable in every node back to the original value of (None, -inf)
        :return: None
        """
        for node in self.nodes:
            node.pminval = ([], float("-inf"))

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

        if CONFIG["testing"]:
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
        if CONFIG["testing"]:
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

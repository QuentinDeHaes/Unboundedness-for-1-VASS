from Node import *

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

    def add_node(self, node):
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
        f.write("  "+self.start_node.dot_value()+'\n')
        while len(to_visit) != 0:
            current = to_visit[0]
            to_visit = to_visit[1:]
            already_visited.add(current)

            for node, amount in current.get_edges():
                if node not in already_added:
                    already_added.add(node)
                    f.write("  "+node.dot_value()+'\n')
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
        excecute the bellman ford algorithm to get shortest path of nodes (will be used as base to find positive cycles
        :return:
        """
        self.start_node.distance = 0
        # bellman ford needs V-1 iterations to certainly have shortest path (without negative cycles)
        for i in range(len(self.nodes)-1):
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
        - the next part is only a single bellamn run so O(E)
        - and the final part is V-1 times O(V³E) so in total O(V⁴E)
        """
        # TODO check possible issue with node being in 2 different cycles
        # TODO possible issue with 2 cycles sharing nodes splitting and coming back with where
        #  split has identical weight but different amount of nodes: can be fixed by making every cycle and
        #  prospective cycle run 1 by one in (and update 1 by 1) but this will end in far less efficiency still
        #

        self.start_node.distance = 0
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
        for i in range(len(self.nodes)-1):

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
                    # making these forloops O(EV³)
                    if edge[0] == cycle[0][-1]:
                        # if the newest node is our first node, the cycle is complete
                        if cycle[0][0] == edge[1]:
                            # the cycle is complete so we add it to complete_cycles
                            complete_cycles.add((cycle[0]+(edge[1],), cycle[1]+ edge[2]))
                        elif edge[1] not in cycle[0]:
                            # the cycle isn't finished so we add it to the new possible cycles,
                            # if a subsidiary cycle is found, that cycle will also be found elsewhere
                            # and we no longer need this part

                            new_possible_cycles.add((cycle[0]+(edge[1],), cycle[1] + edge[2]))
            possible_cycles = new_possible_cycles

        return complete_cycles

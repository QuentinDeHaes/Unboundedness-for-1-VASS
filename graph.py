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
        """
        # TODO check possible issue with node being in 2 different cycles
        # TODO possible fix: use (node_out, node_in, incr), instead of (node_in, incr) to determine cycle and
        #  generate entire cycles by out->in ==out ->in  where incr==incr, this could still have an issue with
        #  multi-cycles on nodes where the incrementations are incorrect because +3 and +6 could become +3 on one and +3 on other
        # issue: smaller value of s4 gets continued to s7, making it think s7 is part of a cycle

        self.start_node.distance = 0
        # bellman ford needs V-1 iterations to certainly have shortest path (without negative cycles)
        for i in range(len(self.nodes) - 1):
            # by going over all nodes and their outgoing edges, we go over all edges
            for node in self.nodes:
                for edge in node.edges:
                    edge[0].update_distance(node.distance - edge[1])
        # with this, we have done the regular bellman ford with negated values
        # now we will check for more changes
        nodes_in_cycles = set()
        # the largest cycle will (in worst case ) have every node in the cycle, and with edges in reverse order,
        # so we'll need to do this V*E times to be certain every cycle_node is found
        for i in range(len(self.nodes)):
            # by going over all nodes and their outgoing edges, we go over all edges
            for node in self.nodes:
                for edge in node.edges:
                    # if ,after already doing entire bellman ford, there still is a change in the distance,
                    # there exists a negative cycle, we will add this new node to the list (t
                    if edge[0].distance > node.distance - edge[1]:

                        nodes_in_cycles.add((edge[0], edge[0].distance - (node.distance - edge[1])))
                        edge[0].update_distance(node.distance - edge[1])

        return nodes_in_cycles

from Node import *


class Graph:
    def __init__(self, start_node: Node):
        self.start_node = start_node
        self.current_node = start_node
        self.z_value = 0

    def to_dot(self, filename):
        f = open(filename, "w")
        # temp_current_node = self.current_node
        # self.current_node = self.start_node
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

        # self.current_node = temp_current_node
        f.close()


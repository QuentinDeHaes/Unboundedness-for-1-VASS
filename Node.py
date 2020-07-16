class Node:
    """
    a single node from our graph
    """
    def __init__(self, id: int):
        self.id = id
        self.disequalities = set()
        self.edges = []

    def set_disequalities(self, disequalities):
        self.disequalities= set(disequalities)

    def get_disequalities(self):
        return self.disequalities

    def add_disequality(self, disequality):
        self.disequalities.add(disequality)

    def get_id(self):
        return self.id

    def add_edge(self, node, z_increase):
        self.edges.append((node, z_increase))

    def get_edges(self):
        return self.edges

    def set_edges(self, edges):
        self.edges = edges

    def dot_value(self):

        val = "\"s{}\"[label = \" s{} ".format(self.id, self.id)
        if len(self.disequalities ) != 0:
            val += "\\n != {} ".format(','.join(str(x) for x in self.disequalities))


        val += "\"]"
        return val


class NodeCreator:
    def __init__(self):
        self.current_id = 0

    def create_node(self):
        node =Node(self.current_id)
        self.current_id += 1
        return node

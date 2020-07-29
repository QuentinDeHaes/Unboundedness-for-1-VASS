import math
class Node:
    """
    a single node from our graph
    """
    def __init__(self, id: int):
        """
        makes a new node, without any outgoing (or ingoing ) edges and no disequalities
        for the bellman-ford algorithm we add a distance from start and set it to infinity
        :param id: the id of the node, needs to be unique for each node of the graph
        """
        self.id = id
        self.disequalities = set()
        self.edges = []
        self.distance = math.inf

    def set_disequalities(self, disequalities):
        """
        set the disequalities of the node
        :param disequalities: the new disequalities of the node
        :return: None
        """
        self.disequalities= set(disequalities)

    def get_disequalities(self):
        """
        get the disequalities of the node
        :return: the disequalities of the node
        """
        return self.disequalities

    def add_disequality(self, disequality):
        """
        add a single disequality to the node
        :param disequality: the disequality to be added
        :return: None
        """
        self.disequalities.add(disequality)

    def get_id(self):
        """
        get the id of the node
        :return: the id of the node
        """
        return self.id

    def add_edge(self, node, z_increase):
        """
        add an outgoing edge to the node
        :param node: the node the edge goes to
        :param z_increase: the amout the counter needs to be increased with when taking this edge
        :return:
        """
        self.edges.append((node, z_increase))

    def get_edges(self):
        """
        get all outgoing edges from the node
        :return: all outgoing edges from the node
        """
        return self.edges

    def set_edges(self, edges):
        """
        set all the outgoing edges of the node
        :param edges: all the new outgoing edges of the node (needs to be in the shape of [(Node, z_increase), ...]
        :return: None
        """
        self.edges = edges

    def get_distance(self):
        """
        get the current distance from start-node
        :return:
        """
        return self.distance

    def set_distance(self, distance):
        """
        set the current distance from start-node
        :param distance:
        :return:
        """
        self.distance = distance

    def update_distance(self, new_distance):
        """
        update the current distance from start-node if new_distance is smaller than current distance
        :param new_distance:
        :return:
        """
        if new_distance< self.distance:
            self.distance = new_distance
        return self.distance

    def dot_value(self):
        """
        get the representation of the node in dot (with it's name and all disequalities represented)
        :return: the string on how to represent the node in dot
        """
        val = "\"s{}\"[label = \" s{} ".format(self.id, self.id)
        if len(self.disequalities ) != 0:
            val += "\\n != {} ".format(','.join(str(x) for x in self.disequalities))
        val += "\"]"
        return val


class NodeCreator:
    """
    a helperclass to create nodes and ensure no double ids
    """
    def __init__(self):
        """
        initialise the first id for a node on 0
        """
        self.current_id = 0

    def create_node(self):
        """
        create a node with a new id, increase counter and return node
        :return: node
        """
        node =Node(self.current_id)
        self.current_id += 1
        return node

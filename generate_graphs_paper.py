from graph import Graph
from Node import Node
from typing import Tuple, List


def generate_1_pos_neg_cyc() -> Tuple[Graph, List[Node]]:
    """
    generate a graph with a positive and a negative cycle linked at a shared node
    :return: Graph, nodes
    """
    s0 = Node(0)
    s1 = Node(1)
    s2 = Node(2)
    s3 = Node(3)
    s1.set_disequalities([60])
    s2.set_disequalities([58])
    s3.set_disequalities([4])
    s0.add_edge(s1, 12)
    s1.add_edge(s2, -12)
    s2.add_edge(s1, 18)
    s1.add_edge(s3, -50)
    s3.add_edge(s1, 49)
    g = Graph(s0)
    g.set_nodes([s0, s1, s2, s3])
    return g, [s0, s1, s2, s3]


def generate_1_pos_cyc() -> Tuple[Graph, List[Node]]:
    """
    generate a graph with a single node returning to itself with value 2
    :return: Graph, nodes
    """
    s0 = Node(0)
    s1 = Node(1)
    s2 = Node(2)
    s1.set_disequalities([60])
    s2.set_disequalities([58])
    s0.add_edge(s1, 12)
    s1.add_edge(s2, -12)
    s2.add_edge(s1, 18)

    g = Graph(s0)
    g.set_nodes([s0, s1, s2])
    return g, [s0, s1, s2]


def generate_lossy_cycle() -> Tuple[Graph, List[Node]]:
    s0 = Node(0)
    s1 = Node(1)
    s2 = Node(2)
    s3 = Node(3)
    s4 = Node(4)
    s5 = Node(5)
    s0.add_edge(s1, 12)
    s1.add_edge(s2, -4)
    s2.add_edge(s1, 18)
    s1.add_edge(s3, 1)
    s3.add_edge(s4, 1)
    s4.add_edge(s5, 1)
    s5.add_edge(s1, 1)
    g = Graph(s0)
    g.set_nodes([s0, s1, s2, s3, s4, s5])
    return g, [s0, s1, s2, s3, s4, s5]

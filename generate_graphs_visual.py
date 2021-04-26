from graph import Graph
from Node import Node
from typing import Tuple, List

"""
ALL of these graphs have a visual version with the same name in the graphs folder
"""

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


def generate_1_pos_neg_cyc_unbounded() -> Tuple[Graph, List[Node]]:
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
    s3.set_disequalities([14])
    s0.add_edge(s1, 12)
    s1.add_edge(s2, -12)
    s2.add_edge(s1, 18)
    s1.add_edge(s3, -40)
    s3.add_edge(s1, 39)
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


def generate_2_pos_cycs() -> Tuple[Graph, List[Node]]:
    """
    generate a graph with a single node returning to itself with value 2
    :return: Graph, nodes
    """
    s0 = Node(0)
    s1 = Node(1)
    s2 = Node(2)
    s3 = Node(3)
    s4 = Node(4)
    s5 = Node(5)
    s6 = Node(6)
    s7 = Node(7)
    s1.set_disequalities([60])
    s2.set_disequalities([58])
    s3.set_disequalities([62])
    s4.set_disequalities([20])
    s5.set_disequalities([10])
    s6.set_disequalities([21])
    s7.set_disequalities([22])
    s0.add_edge(s1, 12)
    s1.add_edge(s2, -12)
    s2.add_edge(s1, 18)
    s2.add_edge(s3, 2)
    s3.add_edge(s4, 5)
    s4.add_edge(s5, -10)
    s5.add_edge(s6, 11)
    s6.add_edge(s7, 1)
    s7.add_edge(s4, 1)

    g = Graph(s0)
    g.set_nodes([s0, s1, s2,s3,s4,s5,s6,s7])
    return g, [s0, s1, s2,s3,s4,s5,s6,s7]




def generate_double_cycle() -> Tuple[Graph, List[Node]]:
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
    s0.add_disequality(500)
    s1.add_disequality(60)
    s2.add_disequality(58)
    s3.add_disequality(61)
    s4.add_disequality(62)
    s5.add_disequality(63)
    g = Graph(s0)
    g.set_nodes([s0, s1, s2, s3, s4, s5])
    return g, [s0, s1, s2, s3, s4, s5]

from graph import Graph
from Node import Node
from typing import Tuple, List


def generate_graph1() -> Tuple[Graph, List[Node]]:
    """
    generate a graph with a single node returning to itself with value 2, and an unreachable disequality
    :return: Graph, nodes
    """
    s0 = Node(0)
    s0.add_edge(s0, 2)
    s0.add_disequality(9)
    g = Graph(s0)
    g.set_nodes([s0])
    return g, [s0]


def generate_graph1_2() -> Tuple[Graph, List[Node]]:
    """
    generate a graph with a single node returning to itself with value 2, and a blocking disequality
    :return: Graph, nodes
    """
    s0 = Node(0)
    s0.add_edge(s0, 2)
    s0.add_disequality(8)
    g = Graph(s0)
    g.set_nodes([s0])
    return g, [s0]

def generate_graph2() -> Tuple[Graph, List[Node]]:
    """
    return a graph of 4 nodes that could acquire every value everywhere, but cannot be 8 anywhere
    :return: Graph, Nodes
    """
    s0 = Node(0)
    s1 = Node(1)
    s2 = Node(2)
    s3 = Node(3)
    s0.add_edge(s1, 0)
    s1.add_edge(s2, 0)
    s1.add_edge(s3, 0)
    s2.add_edge(s0, 2)
    s3.add_edge(s0, -1)
    s0.add_disequality(8)
    s1.add_disequality(8)
    s2.add_disequality(8)
    s3.add_disequality(8)

    g = Graph(s0)
    g.set_nodes([s0, s1, s2, s3])
    return g, [s0, s1, s2, s3]

def generate_graph2_1() -> Tuple[Graph, List[Node]]:
    """
    return a graph of 4 nodes that could acquire every value everywhere, but disequalities block its path
    :return: Graph, Nodes
    """
    s0 = Node(0)
    s1 = Node(1)
    s2 = Node(2)
    s3 = Node(3)
    s0.add_edge(s1, 0)
    s1.add_edge(s2, 0)
    s1.add_edge(s3, 0)
    s2.add_edge(s0, 2)
    s3.add_edge(s0, -1)
    s0.add_disequality(8)
    s1.add_disequality(9)
    s2.add_disequality(9)
    s3.add_disequality(10)

    g = Graph(s0)
    g.set_nodes([s0, s1, s2, s3])
    return g, [s0, s1, s2, s3]

def generate_graph3()-> Tuple[Graph, List[Node]]:
    s0 = Node(0)
    s1 = Node(1)
    s2 = Node(2)
    s3 = Node(3)
    s0.add_edge(s1, 0)
    s1.add_edge(s2, 0)
    s1.add_edge(s3, 0)
    s2.add_edge(s0, 2)
    s3.add_edge(s0, -1)

    g = Graph(s0)
    g.set_nodes([s0, s1, s2, s3])
    return g, [s0, s1, s2, s3]
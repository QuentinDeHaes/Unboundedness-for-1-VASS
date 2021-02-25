from graph import Graph
from Node import Node
from typing import Tuple, List


def generate_graph1() -> Tuple[Graph, List[Node]]:
    """
    generate a graph with a single node returning to itself with value 2
    :return: Graph, nodes
    """
    s0 = Node(0)
    s0.add_edge(s0, 2)
    g = Graph(s0)
    g.set_nodes([s0])
    return g, [s0]


def generate_graph2() -> Tuple[Graph, List[Node]]:
    """
    return a graph of 4 nodes that could acquire every value everywhere
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

    g = Graph(s0)
    g.set_nodes([s0, s1, s2, s3])
    return g, [s0, s1, s2, s3]

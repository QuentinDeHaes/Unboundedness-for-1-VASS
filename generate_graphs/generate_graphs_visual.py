from graph import Graph
from Node import Node
from typing import Tuple, List

"""
ALL of these graphs_visuals have a visual version with the same name in the graphs_visuals folder
"""

def generate_1_pos_neg_cyc():
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
    return g


def generate_1_pos_neg_cyc_unbounded():
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
    return g
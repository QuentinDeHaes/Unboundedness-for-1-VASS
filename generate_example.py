from graph import Graph
from Node import Node, NodeCreator
def generate_example():
    """
    generates the example graph from the paper
    :return: the example graph
    """

    s0 = Node(0)
    s1 = Node(1)
    s2 = Node(2)
    s3 = Node(3)
    s4 = Node(4)
    s5 = Node(5)
    s6 = Node(6)
    s7 = Node(7)
    s8 = Node(8)
    s9 = Node(9)
    s10 = Node(10)
    s11 = Node(11)
    s12 = Node(12)
    s13 = Node(13)

    s0.add_edge(s1, 12)
    s1.add_edge(s2, -12)
    s2.add_edge(s1, 18)
    s1.add_edge(s3, 12)
    s3.add_edge(s4, 30)
    s4.add_edge(s5, -52)
    s5.add_edge(s6, 52)
    s6.add_edge(s4, 9)
    s4.add_edge(s7, 4)
    s7.add_edge(s8, 4)
    s8.add_edge(s9, -3)
    s9.add_edge(s10, 17)
    s10.add_edge(s11, -80)
    s11.add_edge(s12, 81)
    s12.add_edge(s13, 3)
    s13.add_edge(s10, 6)

    s1.add_disequality(60)
    s3.add_disequality(30)
    s4.add_disequality(90)
    s5.add_disequality(41)
    s6.add_disequality(96)
    s7.add_disequality(70)
    s8.add_disequality(80)
    s9.add_disequality(80)
    s10.add_disequality(120)
    s11.add_disequality(43)
    s12.add_disequality(130)
    s13.add_disequality(130)

    g = Graph(s0)
    g.set_nodes([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13])
    return g

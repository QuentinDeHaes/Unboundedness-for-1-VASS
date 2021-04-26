import unittest
from main import Coverability_in_1Vass_w_Disequality_guards
from CONFIG import CONFIG
from generate_graphs import *
from generate_graphs_visual import *


class MyTestCase(unittest.TestCase):
    """ test the entire algorithm on various 1-VASS"""
    CONFIG["testing"] = True

    def test_something(self):
        self.assertNotEqual(True, False)

    def test_graph1(self):
        g, nodes = generate_graph1()
        res = Coverability_in_1Vass_w_Disequality_guards(g, (g.start_node, 0))
        self.assertTrue(res)

    def test_graph1_2(self):
        g, nodes = generate_graph1_2()
        res = Coverability_in_1Vass_w_Disequality_guards(g, (g.start_node, 0))
        self.assertFalse(res)

    def test_graph2(self):
        g, nodes = generate_graph2()
        res = Coverability_in_1Vass_w_Disequality_guards(g, (g.start_node, 0))
        self.assertTrue(res)
        g, nodes = generate_graph2_1()
        res = Coverability_in_1Vass_w_Disequality_guards(g, (g.start_node, 0))
        self.assertFalse(res)

    def test_graphs_visual(self):
        """
        test all the graphs that have a visual representation
        :return:
        """
        g, nodes = generate_1_pos_cyc()
        res = Coverability_in_1Vass_w_Disequality_guards(g, (g.start_node, 0))
        self.assertFalse(res)

        g, nodes = generate_1_pos_neg_cyc()
        res = Coverability_in_1Vass_w_Disequality_guards(g, (g.start_node, 0))
        self.assertFalse(res)

        g, nodes = generate_double_cycle()
        res = Coverability_in_1Vass_w_Disequality_guards(g, (g.start_node, 0))
        self.assertTrue(res)

        g, nodes = generate_2_pos_cycs()
        res = Coverability_in_1Vass_w_Disequality_guards(g, (g.start_node, 0))
        self.assertTrue(res)

        g, nodes = generate_1_pos_neg_cyc_unbounded()
        res = Coverability_in_1Vass_w_Disequality_guards(g, (g.start_node, 0))
        self.assertTrue(res)

        g, nodes = generate_double_cycle2()
        res = Coverability_in_1Vass_w_Disequality_guards(g, (g.start_node, 0))
        self.assertTrue(res)


if __name__ == '__main__':
    unittest.main()

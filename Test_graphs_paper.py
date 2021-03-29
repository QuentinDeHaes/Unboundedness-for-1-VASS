import unittest
import unittest
from graph import Graph
from Node import Node
from generate_example import generate_example
from helper_functions import *
from Closure import Closure
import math
from generate_graphs_paper import generate_1_pos_neg_cyc, generate_lossy_cycle, generate_1_pos_cyc


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_new_graphs(self):
        g, nodes = generate_1_pos_neg_cyc()
        g.bellman_ford_alg()
        cycles = g.get_cycles()
        self.assertEqual(len(cycles), 1, "negative cycle added")

    def test_faulty_cycle(self):
        g, nodes = generate_lossy_cycle()
        g.bellman_ford_alg()
        cycles = g.get_cycles()
        self.assertEqual(len(cycles), 2, "cycle missed")
        print(cycles)

    def test_single_pos_cyc_chains(self):
        g, nodes = generate_1_pos_cyc()
        g.bellman_ford_alg()
        cycles = g.get_cycles()
        g.set_non_allowable_values(cycles)
        chains = g.get_bounded_chains(cycles)
        self.assertEqual(len(cycles), 1, "incorrect cycles located")
        self.assertIn(nodes[1], chains)
        self.assertIn(nodes[2], chains)


if __name__ == '__main__':
    unittest.main()

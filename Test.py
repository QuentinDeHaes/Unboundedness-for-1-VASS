import unittest
from graph import Graph
from Node import Node
from generate_example import generate_example
from helper_functions import *
from Closure import Closure
import math


class MyTestCase(unittest.TestCase):
    g = generate_example()
    s0 = g.start_node
    s1 = s0.get_edges()[0][0]
    s2 = s1.get_edges()[0][0]
    s3 = s1.get_edges()[1][0]
    s4 = s3.get_edges()[0][0]
    s5 = s4.get_edges()[0][0]
    s6 = s5.get_edges()[0][0]
    s7 = s4.get_edges()[1][0]
    s8 = s7.get_edges()[0][0]
    s9 = s8.get_edges()[0][0]
    s10 = s9.get_edges()[0][0]
    s11 = s10.get_edges()[0][0]
    s12 = s11.get_edges()[0][0]
    s13 = s12.get_edges()[0][0]

    def test_base(self):
        self.assertEqual(True, True)
        self.assertEqual(False, False)
        self.assertNotEqual(True, False)

    def test_helper_functions(self):

        value = get_distances_in_path((self.s0, self.s1, self.s3))
        self.assertEqual(value, (12, 12), "distances in the path of nodes does not work")

        value = chain_max_non_cyclables([1, 2, 5, 6, 8, 9, 12], 4, 4)
        compare_dict = {0: 12, 1: 9, 2: 6}
        self.assertEqual(value, compare_dict, "chain_max_non_cyclables not working")

        value = cleanup_non_cyclables([1, 2, 5, 6, 8, 9, 12], 4, 4)
        compare_dict = {0: [8, 12], 1: [5, 9], 2: [6]}
        self.assertEqual(value, compare_dict, "cleanup_non_cyclables not working")

    def test_closure(self):
        clos = Closure(6, 16, 2)
        self.assertEqual(clos.len(), 6, "incorrect length of closure")
        self.assertEqual(clos[0], 6)
        self.assertEqual(clos[1], 8)
        clos2 = Closure(None, 10, 2)
        self.assertEqual(clos2.len(), math.inf, "incorrect length for unbounded closure")
        with self.assertRaises(Exception):
            a = clos[8]
        with self.assertRaises(Exception):
            a = clos2[1]
        self.assertTrue(8 in clos)
        self.assertTrue(15 not in clos)
        self.assertTrue(-60 in clos2)
        self.assertTrue(12 not in clos2)

    def test_bellman_ford(self):
        self.g.bellman_ford_alg()
        self.assertEqual(self.g.start_node.get_distance(), 0)

        self.g.reset_distances()
        for node in self.g.nodes:
            self.assertEqual(node.get_distance(), math.inf)

        self.g.bellman_ford_alg()
        cycles = self.g.get_cycles()
        self.assertEqual(len(cycles), 3, "all 3 cycles are not found")
        for cycle in cycles:
            if cycle[1] == 6:
                self.assertEqual(len(cycle[0]), 3, "short cycle not of correct length")
                self.assertTrue(self.s1 in cycle[0], "s1 not in short cycle")
                self.assertTrue(self.s2 in cycle[0], "s2 not in short cycle")

            if cycle[1] == 9:
                self.assertEqual(len(cycle[0]), 4, "medium cycle not of correct length")
                self.assertTrue(self.s4 in cycle[0], "s4 not in medium cycle")
                self.assertTrue(self.s5 in cycle[0], "s5 not in medium cycle")
                self.assertTrue(self.s6 in cycle[0], "s6 not in medium cycle")

            if cycle[1] == 10:
                self.assertEqual(len(cycle[0]), 5, "long cycle not of correct length")
                self.assertTrue(self.s10 in cycle[0], "s10 not in long cycle")
                self.assertTrue(self.s11 in cycle[0], "s11 not in long cycle")
                self.assertTrue(self.s12 in cycle[0], "s12 not in long cycle")
                self.assertTrue(self.s13 in cycle[0], "s13 not in long cycle")

    def test_nodes(self):
        node = self.s1
        self.assertEqual(node.get_disequalities(), {60}, "get_disequalities incorrect")

        n = node.__copy__()
        self.assertEqual(node.get_disequalities(), n.get_disequalities(), "no correct copy")
        self.assertEqual(node.get_id(), n.get_id(), "no correct copy")
        self.assertEqual(node.get_distance(), n.get_distance(), "no correct copy")
        self.assertEqual(node.get_edges(), n.get_edges(), "no correct copy")

        self.assertIsNone(n.set_distance(50))
        self.assertEqual(n.get_distance(), 50)
        self.assertEqual(n.update_distance(24), 24)
        self.assertEqual(n.get_distance(), 24)

    def test_graph(self):
        graph = self.g
        gcopy = graph.__copy__()

        self.assertEqual(graph.start_node.get_id(), gcopy.start_node.get_id())
        if hasattr(graph, "cycles"):
            self.assertEqual(graph.cycles, gcopy.cycles)


if __name__ == '__main__':
    unittest.main()

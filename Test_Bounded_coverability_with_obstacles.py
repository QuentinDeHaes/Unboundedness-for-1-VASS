import unittest

import Bounded_coverability_with_obstacles
import generate_example
from generate_graphs import *
from CONFIG import CONFIG


class MyTestCase(unittest.TestCase):
    CONFIG['testing'] = True
    g = generate_example.generate_example()
    s0 = g.start_node
    s1 = s0.get_edges()[0][0]
    s2 = s1.get_edges()[0][0]
    s3 = s1.get_edges()[1][0]
    s4 = s3.get_edges()[0][0]

    def test_something(self):
        self.assertNotEqual(True, False)

    def test_bcwo(self):
        O = Bounded_coverability_with_obstacles.O_equationset(52, 6, [1, 2], [63, 75])
        self.assertTrue(
            Bounded_coverability_with_obstacles.Bounded_coverability_with_obstacles((self.g.start_node, 0),
                                                                                    self.s4,
                                                                                    self.g.BoundedCoverWithObstacles_GetL(),
                                                                                    O))

    def test_bwco2(self):
        # secretly allow no value without stating it directly
        O2 = Bounded_coverability_with_obstacles.O_equationset(52, 6, [0, 1, 2, 3, 4, 5], [63, 75])
        self.assertFalse(
            Bounded_coverability_with_obstacles.Bounded_coverability_with_obstacles((self.g.start_node, 0),
                                                                                    self.s4,
                                                                                    self.g.BoundedCoverWithObstacles_GetL(),
                                                                                    O2))

    def test_bwco3(self):
        g2, nodes = generate_graph1()
        O2 = Bounded_coverability_with_obstacles.O_equationset(52, 2, [0], [63, 75])
        O3 = Bounded_coverability_with_obstacles.O_equationset(52, 2, [1], [63, 75])
        self.assertFalse(
            Bounded_coverability_with_obstacles.Bounded_coverability_with_obstacles((nodes[0], 0),
                                                                                    nodes[0],
                                                                                    g2.BoundedCoverWithObstacles_GetL(),
                                                                                    O2))
        self.assertTrue(
            Bounded_coverability_with_obstacles.Bounded_coverability_with_obstacles( (nodes[0], 0),
                                                                                    nodes[0],
                                                                                    g2.BoundedCoverWithObstacles_GetL(),
                                                                                    O3))

    def test_bwco4(self):
        g2, nodes = generate_graph2()
        O2 = Bounded_coverability_with_obstacles.O_equationset(52, 2, [0], [63, 75])
        O3 = Bounded_coverability_with_obstacles.O_equationset(52, 2, [1], [63, 75])
        O4 = Bounded_coverability_with_obstacles.O_equationset(52, 2, [0, 1], [63, 75])
        self.assertTrue(
            Bounded_coverability_with_obstacles.Bounded_coverability_with_obstacles((nodes[0], 0),
                                                                                    nodes[0],
                                                                                    g2.BoundedCoverWithObstacles_GetL(),
                                                                                    O2))
        self.assertTrue(
            Bounded_coverability_with_obstacles.Bounded_coverability_with_obstacles((nodes[0], 0),
                                                                                    nodes[0],
                                                                                    g2.BoundedCoverWithObstacles_GetL(),
                                                                                    O3))
        self.assertFalse(
            Bounded_coverability_with_obstacles.Bounded_coverability_with_obstacles( (nodes[0], 0),
                                                                                    nodes[0],
                                                                                    g2.BoundedCoverWithObstacles_GetL(),
                                                                                    O4))


if __name__ == '__main__':
    unittest.main()

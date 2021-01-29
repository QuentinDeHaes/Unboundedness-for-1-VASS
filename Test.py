import unittest
from graph import Graph
from  Node import Node
from generate_example import generate_example
from helper_functions import *

class MyTestCase(unittest.TestCase):

    g = generate_example()

    def test_base(self):
        self.assertEqual(True, True)
        self.assertEqual(False, False)
        self.assertNotEqual(True, False)

    def test_helper_functions(self):
        s0 = self.g.start_node
        s1 = s0.get_edges()[0][0]
        s3 = s1.get_edges()[1][0]
        value = get_distances_in_path((s0, s1, s3))
        self.assertEqual(value, (12,12), "distances in the path of nodes does not work")


        value = chain_max_non_cyclables([1,2,5,6,8,9,12], 4, 4)
        compare_dict = {0:12, 1:9, 2:6}
        self.assertEqual(value, compare_dict, "chain_max_non_cyclables not working")

        value = cleanup_non_cyclables([1, 2, 5, 6, 8, 9, 12], 4, 4)
        compare_dict = {0: [8, 12], 1: [5, 9], 2: [6]}
        self.assertEqual(value, compare_dict, "cleanup_non_cyclables not working")


if __name__ == '__main__':
    unittest.main()

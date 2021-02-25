from graph import Graph
from Node import Node
from typing import Tuple, List


class O_equationset:
    """
    the equationset as given by equation (4) defined by different non-negative integers
    """

    def __init__(self, l: int, W: int, a_i: List[int], b_i: List[int]):
        self.l = l
        self.W = W
        self.a_i = a_i
        self.b_i = b_i

    def __contains__(self, item):
        if item < self.l:
            return False
        for a in self.a_i:
            if (item - a) % self.W == 0:
                return False
        for b in self.b_i:
            if item == b:
                return False
        return True


class Un:
    """
    the complete representation of Un required in the BoundedCoverWObstacles sub-routine
    """

    def __init__(self, complement):
        """Initialize U_0 by using it's complement, the complement is given as a set of closures"""
        self.O_i = set()

    def add_residue_class(self, O: O_equationset):
        self.O_i.add(O)

    def __contains__(self, item):
        for o in self.O_i:
            if item in o:
                return True

        return False

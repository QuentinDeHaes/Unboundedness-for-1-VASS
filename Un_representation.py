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

    def __init__(self,g, cycles, complement):
        """Initialize U_0 by using it's complement, the complement is given as a set of closures"""
        self.O_i = set()

        for cycle in cycles:
            W = cycle[1]
            for node in cycle[0][:-1]:
                l = node.minimal_cyclable[g.cycles[cycle]]
                a_i = []
                for closure in complement[node]:
                    if closure.step == W:
                        #TODo check whether the closure is actually from the cycle using l and minvalue sort off
                        a_i.append(closure.minVal % W)
                O_i = O_equationset(l,W,a_i, [])
                self.O_i.add((node,O_i))


    def add_residue_class(self, O: O_equationset):
        self.O_i.add(O)

    def __contains__(self, item: Tuple):

        for o in self.O_i:
            if item[0] != o[0]:
                return False
            if item[1] in o[1]:
                return True

        return False

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
        self.O_i2 = dict()

        for cycle in cycles:
            W = cycle[1]
            for node in cycle[0][:-1]:
                l = node.minimal_cyclable[g.cycles[cycle]]
                a_i = []
                other_O_is = dict((int, int))
                for closure in complement[node]:
                    if closure.step == W:
                        #TODo check whether the closure is actually from the cycle using l and minvalue sort off
                        a_i.append(closure.minVal % W)
                        other_O_is[closure.minVal % W] = max(closure.maxVal + W, other_O_is[closure.minVal % W])

                O_i = O_equationset(l,W,a_i, [])
                self.O_i.add((node,O_i))
                for closure in other_O_is:
                    bc = list(a_i)
                    bc.remove(closure)
                    O_i = O_equationset(other_O_is[closure], W , bc, [])
                    self.O_i2[node][cycle][closure] = O_i



    def add_residue_class(self, O: O_equationset):
        self.O_i.add(O)

    def __contains__(self, item: Tuple):

        for o in self.O_i:
            if item[0] != o[0]:
                continue
            if item[1] in o[1]:
                return True
        if item[0] not in self.O_i2:
            return False
        for attempt in self.O_i2[item[0]]:
            if item[1]% attempt[1] in self.O_i2[item[0]][attempt]:
                if item[1] in self.O_i2[item[0]][attempt][item[1]% attempt[1]]:
                    return True


        return False

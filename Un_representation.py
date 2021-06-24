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
        """
        check whether the O_equationset contains item
        :param item: the item to check
        :return: bool
        """
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

    def __init__(self, g, complement):
        """
        Initialize U_0 by using it's complement, the complement is given as a set of closures
        :param g: the graph
        :param complement: the complement of U_n, i.e. a list of bounded chains
        """
        self.O_i = set()  # Where we add the trivial q-residue classes
        self.O_i2 = dict()  # Where we add the non-trivial q-residue classes in a dict node -> dict(cycle-> O_i)

        # for cycle in cycles:  # Loop over all cycles
        #     W = cycle[1]  # Get the weight of each cycle
        #     for node in cycle[0][:-1]:  # loop over each (unique) node in the cycle
        for node in g.nodes_in_cycles:
            W = node.optimal_cycle[1]
            if node not in self.O_i2:  # initialise the node in the O_i2 dict if not yet done
                self.O_i2[node] = dict()
                # generate all values nescessary to generate the various values
            l = node.minimal_cyclable
            a_i = []
            other_O_is = dict()
            for closure in complement[node]:  # go over each bounded chain in the complement
                if closure.step == W:
                    a_i.append(closure.minVal % W)
                    other_O_is[closure.minVal % W] = max(closure.maxVal + W,
                                                         0 if other_O_is.get(closure.minVal % W) is None else
                                                         other_O_is[closure.minVal % W])

            O_i = O_equationset(l, W, a_i, [])
            self.O_i.add((node, O_i))
            for closure in other_O_is:
                bc = list(a_i)
                bc.remove(closure)
                O_i = O_equationset(other_O_is[closure], W, bc, [])
                self.O_i2[node][closure] = O_i

    def add_residue_class(self, O: O_equationset) -> None:
        """
        add a O_equationset to the O_s set
        :param O: the O_equationset
        :return:
        """
        self.O_i.add(O)

    def __contains__(self, item: Tuple) -> bool:
        """
        return True if item is in any if the O_equationsets
        :param item: the item (tuple of node, value) for which we check whether we contain it
        :return: bool True if contains False otherwhise
        """

        for o in self.O_i:
            if item[0] != o[0]:
                continue
            if item[1] in o[1]:
                return True
        if item[0] not in self.O_i2:
            return False
        for attempt in self.O_i2[item[0]]:
            if item in self.O_i2[item[0]][attempt]:
                return True
            # if item[1] % attempt[1] in self.O_i2[item[0]][attempt]:
            #     if item[1] in self.O_i2[item[0]][attempt][item[1] % attempt[1]]:
            #         return True

        return False

    def list_O_i(self) -> list:
        """

        :return: a list of all O_is in our U_n object
        """
        return_val = list(self.O_i)

        for node in self.O_i2:
            for a_i in self.O_i2[node]:
                return_val.append((node, self.O_i2[node][a_i]))

        return return_val

    def edit_non_triv_q_residueclass(self, node, W, allowed_a_i, new_minval, all_chains):
        """
        edit a non-trivial residue class (possibly allowing more values to be seen)
        :param node: the node for which the residue class needs to be edited
        :param W: the wheigt of the class
        :param allowed_a_i:  the allowed a_i from the non-triv q-res classes for this specific chain
        :param new_minval: the new minimal value allowed
        :param all_chains: a list of all (currently) bounded chains
        :return:the newly edited q-residue class in form of an O_equationset
        """
        if node.optimal_cycle[1] == W:
            if allowed_a_i in self.O_i2[node]:
                new_minval2 = min(new_minval, self.O_i2[node][allowed_a_i].l)
                new_bi = []
                for chain in all_chains:
                    if chain.step == W and chain.minVal >= new_minval2:
                        new_bi += chain.get_index_list(0, chain.len())
                new_oi = O_equationset(new_minval2, W, self.O_i2[node][allowed_a_i].a_i, new_bi)
                self.O_i2[node][allowed_a_i] = new_oi
                return new_oi

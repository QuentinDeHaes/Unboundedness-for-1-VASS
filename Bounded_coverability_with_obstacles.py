from graph import Graph
from Node import Node
from typing import Tuple, List
from Un_representation import O_equationset


def prune(reachable_in_k, L, m, n, W):
    """
    method used to prune after each step of the coverability algorithm
    :param reachable_in_k: the values the coverability method generated with a single step
    :return: the pruned version of the method
    """

    reachable_dict = dict()
    # turn the set of reachable values in a dict per state to make it easier to prune (as pruning is done as max per state)
    for value in reachable_in_k:
        if value[0] not in reachable_dict:
            reachable_dict[value[0]] = []
        reachable_dict[value[0]].append(value[1])

    # sort the values for each node from biggest to smallest
    for key in reachable_dict:
        reachable_dict[key] = sorted(reachable_dict[key], reverse=True)

    reachable_dict = _prune_congruence(reachable_dict, L, n, W)
    reachable_dict = _prune_maximum(reachable_dict, L, m, n)

    new_reachable = set()
    for key in reachable_dict:
        for item in reachable_dict[key]:
            new_reachable.add((key, item))

    return new_reachable


def _prune_congruence(reachable_in_k, L, n, W):
    """
    the first pruning step of the algorithm
    :param reachable_in_k: the original set of reachable values to be pruned

    :param L:
    :param n:
    :return:
    :return: the pruned reachable_in_k
    """

    for key in reachable_in_k:
        dic = dict()
        for value in reachable_in_k[key]:
            if value % W not in dic:
                dic[value % W] = []

            dic[value % W].append(value)
        all_remaining_vals = list()
        for key2 in dic:
            dic[key2] = sorted(dic[key2])
            dic[key2] = dic[key2][: min(len(dic[key2]), n + L)]
            all_remaining_vals += dic[key2]

        reachable_in_k[key] = all_remaining_vals

    return reachable_in_k


def _prune_maximum(reachable_in_k, L, m, n):
    """
    the second pruning step where we get only the highest (n+L)*(m+1) values
    :param reachable_in_k:
    :param L:
    :param m:
    :param n:
    :return:
    """
    for key in reachable_in_k:
        reachable_in_k[key] = sorted(reachable_in_k[key], reverse=True)[
                              : min(len(reachable_in_k[key]), (n + L) * (m + 1))]

    return reachable_in_k


def getAllReachable1Step(original_nodes):
    """
    return all node, value pairs reachable from any of the pairs in the original nodes in a single step
    :param original_nodes: a set of node, value, complete_path pairs from which we check what they can reach in 1 step
    :return: a set of node, value pairs that can be reached from any of original_nodes in a single step
    """
    reachable = set()
    for node in original_nodes:  # for each node in our set, we gather it's reachable states and add them to our result
        lis = node[0].get_edges()
        for new_node in lis:  # a newly reachable node is only reachable by another node, each node can only have V-1 O(V) outgoing edges
            if node[1] + new_node[1] >= 0:
                # check if this node does not infringe upon any disequalities or other rules
                tup = (new_node[0], node[1] + new_node[1])
                # check if the new node does not possess any cycles in it O(L*V³)
                reachable.add(tup)

    return reachable


def Bounded_coverability_with_obstacles(g: Graph, source: Tuple[Node, int], target_state: Node, L: int,
                                        O: O_equationset) -> bool:
    """
    the method to see whether the node :source: can reach configuration (targetstate, o ) o∈ O
    :param g: the graph we are checking in
    :param source:the source configuration
    :param target_state:the target state
    :param L:a value generated based on the amount of nodes in the graph
    :param O: a special set of infinite values
    :return:Bool can source reach a conf (t, o)
    """

    reachable = {source}

    for i in range(L):  # the arlorithm runs for at most L rounds
        if len(reachable) == 0:
            return False
        unpruned_reachable = getAllReachable1Step(reachable)
        for val in unpruned_reachable:
            if val[0] == target_state and val[1] in O:
                return True

        reachable = prune(unpruned_reachable, L, len(O.a_i), len(O.b_i), O.W)

    return False

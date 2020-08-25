import Node
import graph


def get_distances_in_path(path: tuple):
    """
    give a path of nodes, it will give the weight of the edges between each of the nodes
    :param path: a tuple of nodes with edges between them ex: (node1, node2, node3)
    :return: a tuple of size len(path)-1 with the weight of the edge between node i and i+1 (with 0<=i<len(path))
    this method is O(X* E) withX being the size of the path
    """
    distances = []
    for i in range(len(path) - 1):
        found = False
        for edge in path[i].edges:
            if edge[0].id == path[i + 1].id:
                distances.append(edge[1])
                found = True
                break
        if not found:
            # there is no edge from node i to node i+1
            return False
    return tuple(distances)


def set_non_allowable_values(complete_cycles):
    """
    set on each node on which values, the cycle can't be taken
    :param complete_cycles: the cycles as received by the get_cycles method
    :return:None (the changes happen on the node-classes)
    this code is O(V⁴)
    """
    # TODO ensure node within 2 cycles does not overwrite the not_allowed
    # per cycle we run this code (at most O(V²))
    for cycle in complete_cycles:

        # distances is O(V*E)
        distances = get_distances_in_path(cycle[0])

        # for each node in the cycle we run this the code (this loop  is O(V))
        for node_i in range(len(cycle[0]) - 1):
            not_allowed = []
            current_add = 0

            not_allowed += [num - cycle[1] for num in cycle[0][:-1][node_i].get_disequalities()]
            current_add += distances[node_i % (len(cycle[0]) - 1)]
            # we run over every edge in the cycle (also O(V))
            for j in range(1, len(distances)):
                not_allowed += [num - current_add for num in
                                cycle[0][:-1][(node_i + j) % (len(cycle[0]) - 1)].get_disequalities()]

                current_add += distances[(node_i + j) % (len(cycle[0]) - 1)]
            cycle[0][node_i].non_cyclables = not_allowed

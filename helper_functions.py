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


def cleanup_non_cyclables(non_cyclables, cyclabe_increase: int, minimal_cyclable: int):
    """
    clean the non_cyclables so that each chain has only one value, and each value below minimal is removed
    :param non_cyclables: the disequalities whether we allow taking the cycle
    :param cyclabe_increase: the amount with which the countervalue increased when taking the cycle
    :param minimal_cyclable: the minimal countervalue to take the value
    :return: a dict where each chain has it's own bounded value
    O(V) if maximum amount of disequalities per node is fixed
    # the amount of chains that are bounded is also limited by the minimum between the positive_cycle_value
    # and the amount of disequalities, which makes us bounded by O(V) as long as
    # the amount of disequalities is fixed
    """
    cleaned_non_cyclables = dict()
    for non_cyclable in non_cyclables:
        if non_cyclable < minimal_cyclable:
            continue

        value = (non_cyclable % cyclabe_increase)

        if value in cleaned_non_cyclables:
            if non_cyclable > cleaned_non_cyclables[non_cyclable % cyclabe_increase]:
                cleaned_non_cyclables[value] = non_cyclable

        else:
            cleaned_non_cyclables[value] = non_cyclable

    return cleaned_non_cyclables

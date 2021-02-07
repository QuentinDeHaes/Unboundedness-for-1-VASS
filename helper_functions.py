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


def chain_max_non_cyclables(non_cyclables, cyclabe_increase: int, minimal_cyclable: int):
    """
    clean the non_cyclables so that each chain has only one value, the highest, and each value below minimal is removed
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


def DEPRECATED_cleanup_non_cyclables_DEPRECATED(non_cyclables, cyclabe_increase: int, minimal_cyclable: int):
    """
    DEPRECATED
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


def cleanup_non_cyclables(non_cyclables, cyclabe_increase: int, minimal_cyclable: int):
    """
    clean the non_cyclables so that each chain has it's non-allowed values ordered
    :param non_cyclables: the disequalities whether we allow taking the cycle
    :param cyclabe_increase: the amount with which the countervalue increased when taking the cycle
    :param minimal_cyclable: the minimal countervalue to take the value
    :return: a dict where each chain has it's own bounded value
    O(V²) if maximum amount of disequalities per node is fixed because of sort
    # the amount of chains that are bounded is also limited by the minimum between the positive_cycle_value
    # and the amount of disequalities, which makes us bounded by O(V) as long as
    # the amount of disequalities is fixed
    """
    cleaned_non_cyclables = dict()
    for non_cyclable in non_cyclables:

        # values not cyclable because they would cause negative counter need not be considered
        if non_cyclable < minimal_cyclable:
            continue

        value = (non_cyclable % cyclabe_increase)  # check which chain we need to consider

        if value in cleaned_non_cyclables:  # check wether th chain already has values or not

            cleaned_non_cyclables[value].append(non_cyclable)

        else:
            cleaned_non_cyclables[value] = [non_cyclable]

        for key in cleaned_non_cyclables:  # in the end, we need all values in a sorted order, so we'll simply sort at the end
            cleaned_non_cyclables[key] = sorted(cleaned_non_cyclables[key])

    return cleaned_non_cyclables


def get_all_nodes_from_cycles(complete_cycles):
    """
    return all nodes in any of the complete cycles as a set
    :param complete_cycles: the frequently used list of all cycles in the graph
    :return: a set of all nodes present in 1 or more cycles
    """
    all_node = set()
    for cycle in complete_cycles:
        for node in cycle:
            all_node.add(node)

    return all_node

def turn_cycle(cycle, front_node):
    """
    turn the list of the cycle to ensure frontnode is the first
    :param cycle: the cycle to be turned
    :param front_node: the node that needs to be at the front(and the back)
    :return: the turned cycle
    takes at most cyclelength -1 runs, so is bounded by O(V)
    """
    while cycle[0] != front_node:
        del cycle[0]
        cycle.append(cycle[0])
    return cycle

def check_primitive(value, complete_cycles):
    """
    return wether a path has no positive cycles in it
    :param value: the value with a path to be checked
    :param complete_cycles: complete list of all positive cycles in the graph
    :return: BOOL is the path primitive
    for each cycle, check whether it is in the path, you need to run over the path, but pathlength is bounded by L
    so we have O(L*V³)
    """
    for cycle in complete_cycles:
        newlis= value[2]+(value[0],)
        node_i = 0
        while node_i < len(newlis):
            if newlis[node_i] in cycle:
                new_cycle = turn_cycle(cycle, newlis[node_i])
                is_cycle = True
                for j in range(1, len(new_cycle)):
                    if newlis[node_i+j] != new_cycle[j]:
                        is_cycle = False
                        node_i = node_i+j-1
                        break
                if is_cycle:
                    return False

            node_i+=1
    return True




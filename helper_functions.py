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
    for i in range(len(path)-1):
        found = False
        for edge in path[i].edges:
            if edge[0].id == path[i+1].id:
                distances.append(edge[1])
                found = True
                break
        if not found:
            # there is no edge from node i to node i+1
            return False
    return tuple(distances)

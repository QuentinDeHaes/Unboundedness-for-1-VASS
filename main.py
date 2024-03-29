from CONFIG import CONFIG
import sys
import importlib


def Coverability_in_1Vass_w_Disequality_guards(g, source, print_closures=False):
    cycles = g.get_cycles()
    if print_closures:
        for c in cycles:
            print('cycle with {} nodes and weight {} and node_ids:'.format(len(c[0]) - 1, c[1]), end='')
            print(c[0][0].id, end='')
            for i in range(1, len(c[0]) - 1):
                print(',{}'.format(c[0][i].id), end='')

            print('')

    g.set_non_allowable_values(cycles)
    # g.get_unbounded_chains()
    # g.to_dot("dot.dot")
    chains = g.get_bounded_chains()
    if print_closures:
        print("all bounded chains:")
        for chain in chains:
            print("node {}:".format(chain.id))
            for ch in chains[chain]:
                print(ch)
    new_chains, n = g.Unbounded(chains)
    if print_closures:
        print("==================================================")
        print("all values in positive cycles not in Un as chains:")
        for chain in new_chains:
            print("node {}:".format(chain.id))
            for ch in new_chains[chain]:
                print(ch)
    # is_reachable = g.coverable(source, new_chains, cycles, n)
    is_reachable = g.coverable((source), g.BoundedCoverWithObstacles_GetL())
    return is_reachable


if __name__ == "__main__":

    try:
        # print(sys.argv)
        module = importlib.import_module(sys.argv[1])
        function = getattr(module, sys.argv[2])
        g = function()
    except:
        raise Exception("unable to acquire graph function")

    try:
        debug_print = sys.argv[3].lower() == 'true'
    except:
        debug_print = False

    try:

        CONFIG["testing"] = sys.argv[4].lower() == 'true'
    except:
        CONFIG["testing"] = False
    # g = generate_example()

    # g.to_dot("dot.dot")
    is_reachable = Coverability_in_1Vass_w_Disequality_guards(g, (g.start_node, 0), debug_print)
    print("Is the 1-VASS unbounded?:{}".format(is_reachable))

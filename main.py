from Node import *
from graph import *
from generate_example import *
from generate_graphs_paper import generate_1_pos_neg_cyc
from CONFIG import CONFIG


def Coverability_in_1Vass_w_Disequality_guards(g, source, print_closures=False):
    cycles = g.get_cycles()
    g.set_non_allowable_values(cycles)
    # g.get_unbounded_chains()
    # g.to_dot("dot.dot")
    chains = g.get_bounded_chains()
    new_chains, n = g.bndCoverWObstacles(cycles, chains)
    if print_closures:
        print("all values not in Un in chains:")
        for chain in new_chains:
            print("node {}:".format(chain.id))
            for ch in new_chains[chain]:
                print(ch)
    # is_reachable = g.coverable(source, new_chains, cycles, n)
    is_reachable = g.coverable((source), g.BoundedCoverWithObstacles_GetL())
    return is_reachable


if __name__ == "__main__":
    CONFIG["testing"]=True
    g = generate_example()

    g.to_dot("dot.dot")
    is_reachable = Coverability_in_1Vass_w_Disequality_guards(g, (g.start_node, 0), True)
    print("Is the 1-VASS unbounded?:{}".format(is_reachable))

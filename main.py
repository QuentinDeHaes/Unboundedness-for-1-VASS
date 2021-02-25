from Node import *
from graph import *
from generate_example import *

def Coverability_in_1Vass_w_Disequality_guards(g, source):
    g.bellman_ford_alg()
    cycles = g.get_cycles()
    g.set_non_allowable_values(cycles)
    g.get_unbounded_chains(cycles)
    g.to_dot("dot.dot")
    chains = g.get_bounded_chains(cycles)
    new_chains, n = g.bndCoverWObstacles(cycles, chains)
    is_reachable = g.coverable(source, new_chains, cycles, n)
    return is_reachable

if __name__ == "__main__":
    g = generate_example()
    g.to_dot("dot.dot")
    is_reachable=Coverability_in_1Vass_w_Disequality_guards(g, (g.start_node, 0))
    print(is_reachable)

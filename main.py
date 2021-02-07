from Node import *
from graph import *
from generate_example import *

if __name__ == "__main__":
    g = generate_example()
    g.to_dot("dot.dot")
    g.bellman_ford_alg()
    cycles = g.get_cycles()
    g.set_non_allowable_values(cycles)
    g.get_unbounded_chains(cycles)
    g.to_dot("dot.dot")
    chains = g.get_bounded_chains(cycles)
    new_chains = g.getBoundedCoverWithObstacles(cycles, chains)
    is_reachable = g.coverable((g.nodes[0],0), new_chains, cycles)
    print(is_reachable)

from Node import *
from graph import *
from generate_example import *

if __name__ == "__main__":
    g = generate_example()
    g.to_dot("dot.dot")
    g.bellman_ford_alg()
    cycles = g.get_cycles()
    g.set_non_allowable_values(cycles)
    g.to_dot("dot.dot")

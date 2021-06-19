# Unboundedness for 1-VASS
 in this project, we calculate in polynomial time wether a 1-counter graph with disequality guards for the nodes can reach unboundedness
 The theory behind the algorithm can be found [here](https://doi.org/10.4230/LIPIcs.CONCUR.2020.38)
 
 ### usage
 In order to use the project, a proper graph object needs to be written in python to represent your graph and returned in a function.
 An example on how to create such a graph can be found [here](./generate_graphs/generate_example)
 #### command
 Once the graph is created, a single command needs to be run for running the algorithm:
 
 > python main.py \[module_name\] \[function_name\] \[True/False (optional)\] \[True/False (optional)\]


 set the first boolean as True if you wish to acquire extra debug information regarding the algorithm
 default = False
 
 set the second boolean as True if tou wish to significantly reduce the size of the polynomial, 
 smaller polynomial does not ensure correctness if False is returned as unboundedness, but with simpler graphs it can greatly reduce time of algorithm
 default = False
 
 ##### example
  >python main.py generate_graphs.generate_example generate_example True True


 ### tests
 all the tests can be found in the tests folder and can be run from 
 >run_tests.sh

 
  

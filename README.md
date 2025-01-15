# Algorithm-Engineering

This repository provides Python implementations of two ranking algorithms that utilize closeness centrality. The goal of this project is to experimentally analyze the algorithms presented in this [article](https://link.springer.com/chapter/10.1007/978-3-540-69311-6_21).

## Requirements

To run the code in this repository you need:
* Install python3 and pip3
* The following Python libraries
  * networkx
  * numpy
  * matplotlib
  * pandas

  You can install all the required libraries with the following command:
  pip3 install -r requirements.txt

## Execution

1. Clone the repository: git clone https://github.com/sicchio99/Algorithm-Engineering
2. Navigate to the repository directory: cd Algorithm-Engineering
3. Run specific commands as explained in the next sections to execute specific funcitons

### Graphs Generation

To generate graphs, you need to edit the script Graph_generator.py located in the graph_generators folder.
1. Access the graph_generators folder.
2. Edit the file. To specify the number of nodes, modify line 39 by inserting the desired number of nodes for the graphs to be generated inside square brackets.
3. Run the script using the command "python3 Graph_generator.py". The generated graphs will be saved in the graphs folder.

Note: To use the graphs in an experiment, you first need to calculate the exact solution following the steps described in the next section.

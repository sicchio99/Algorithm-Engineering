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

To generate graphs, you need to edit end execute the script Graph_generator.py located in the graph_generators folder.
1. Access the graph_generators folder with the command "cd graph_generators".
2. Edit the file. To specify the number of nodes, modify line 37 by inserting the desired number of nodes for the graphs to be generated inside square brackets.
3. Run the script using the command "python3 Graph_generator.py". The generated graphs will be saved in the graphs folder.

Note: To use the graphs in an experiment, you first need to calculate the exact solution following the steps described in the next section.

Note: If a graph with the entered name already exists, the graph in the graphs folder will be replaced with the new one.

### Calculation of Exact Solutions

To calculate the exact solutions for a graph, you need to edit and run the script ExactAlg.py located in the main directory.
1. Edit the file.
   1. Choose the graph. Modify line 49 by replacing it with the path to the graph to be computed. For graphs generated via the generator, simply replace the number in the name with the number of nodes entered in the generator.
   2. Choose where to save the result. Modify line 71 by entering the output file name where you want to save the result.
2. Run the script using the command "python3 ExactAlg.py".

The result files will be saved in the exact_results directory.

Note: If files with the same name already exist and you save with the same name, the previous file will be overwritten.

### Single Ranking Algorithm Execution

The process to execute one of the two ranking algorithms is very similar. You need to edit and run the file corresponding to the script you want to execute.
1. Access the algorithms folder using the command "cd algorithms".
2. Edit the algorithm file.
  * **Case: Toprank**
    1. Choose the graph. Modify line 57 by inserting the path to the graph to be analyzed.
    2. Choose the number of top vertices. Modify line 65 by replacing the value of k with the number of ranking positions you want to retrieve.
    3. Execute the script using the command "python3 Toprank.py".

  * **Case: Toprank2**
    1. Choose the graph. Modify line 83 by inserting the path to the graph to be analyzed.
    2. Choose the number of top vertices. Modify line 91 by replacing the value of k with the number of ranking positions you want to retrieve.
    3. Execute the script using the command "python3 Toprank2.py".

Note: The results of these two scripts are not saved but can be viewed in the execution logs.

### Experiment Execution

To run an experiment, the following prerequisites must be met:

* The graphs folder must contain only the graphs you want to analyze.
* The exact_results folder must contain the exact solutions of the graphs you want to analyze.

If any of these requirements are not met, refer to the sections "**Graphs Generation**" and "**Calculation of Exact Solution**".

If the prerequisites are satisfied, you can proceed with editing and executing the experiment file.
1. Edit the Experiment.py file located in the main folder. Modify line 69 by inserting the values of k you want to test inside the square brackets.
2. Run the script using the command "python3 Experiment.py".

To view the experiment results, access the experiment_results folder and then the exp_code folder, where code is a numeric value displayed at the end of the experiment execution.
Inside this folder, you will find:
* Graphs showing the temporal performance of the two algorithms.
* Graphs showing the differences between the calculated solutions and the exact ones.
* Summary tables obtained by fixing either the values of k or the number of nodes.

Note: An experiment set up with the default configuration lasts approximately 10.5 hours.

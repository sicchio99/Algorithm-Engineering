import pickle
import RAND as rand
from datetime import datetime
import networkx as nx
# import random
# import matplotlib.pyplot as plt
import numpy as np
# import Graph_generator as Gg
import RAND as rand
import pickle  # Per la serializzazione del grafo
from collections import defaultdict
import math


def rand_and_order_vertices_by_average_distance(G):
    # Step 1: Stima della distanza media (inversa della centralità)
    l = int((G.number_of_nodes() ** (2 / 3)) / (math.log(G.number_of_nodes()) ** (1 / 3)))
    avg_distances, sampled_nodes = rand.randAlgorithm(G, l)

    # Step 2: Ordina i vertici in base alla distanza media (crescente)
    sorted_vertices = sorted(avg_distances.items(), key=lambda item: item[1])

    return sorted_vertices, sampled_nodes

def Toprank(G, k):
    # Ordinamento dei vertici sulla base delle distanze medie stimate.
    # Sorted_vertices è una lista ordinata di tuple (vertex_name, avg_distance)
    sorted_vertices, sampled_nodes = rand_and_order_vertices_by_average_distance(G)

    # Stampa i primi 10 vertici ordinati in base alla loro distanza media stimata
    for index, (vertex, avg_distance) in enumerate(sorted_vertices[:10], start=1):
        print(f"v{index}: Node {vertex}, Estimated Average Distance: {avg_distance}")


with open(f"graphs/graph_test1.pkl", "rb") as f:
    G = pickle.load(f)

num_nodi = G.number_of_nodes()
print(f"Il grafo ha {num_nodi} nodi.")
num_arch = G.number_of_edges()
print(f"Il grafo ha {num_arch} archi.")
k = 10

Toprank(G, k)

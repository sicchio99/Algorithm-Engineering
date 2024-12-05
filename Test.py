import pickle

with open(f"graphs/graph_test9.pkl", "rb") as f:
    G = pickle.load(f)

num_nodi = G.number_of_nodes()
print(f"Il grafo ha {num_nodi} nodi.")
num_arch = G.number_of_edges()
print(f"Il grafo ha {num_arch} archi.")
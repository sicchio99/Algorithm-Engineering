import networkx as nx
import random


def create_connected_weighted_graph(num_nodes):
    # Grafo vuoto
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))

    # Creazione albero per assicurare che il grafo sia connesso
    for i in range(num_nodes - 1):
        weight = random.randint(1, 10)  # Peso casuale agli archi
        G.add_edge(i, i + 1, weight=weight)

    # Aggiunta ulteriori archi casuali per aumentare la densità del grafo
    additional_edges = num_nodes  # numero di archi extra che vogliamo aggiungere
    while additional_edges > 0:
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u != v and not G.has_edge(u, v):  # Evitiamo cicli e duplicati
            weight = random.randint(1, 10)
            G.add_edge(u, v, weight=weight)
            additional_edges -= 1

    return G

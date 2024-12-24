import networkx as nx
import random
import os
import pickle

"""
Generatore di grafi Barabási-Albert per reti sociali.
Realizza grafi connessi, orientati e pesati
Il parametro m determina direttamente la densità del grafo.
"""


def generate_graph(n, m):
    # Genera un grafo BA non orientato
    ba_graph = nx.barabasi_albert_graph(n=n, m=m)

    # Converti in un grafo direzionato
    ba_directed = nx.DiGraph(ba_graph)

    # Aggiungi pesi casuali agli archi per simulare forza della connessione
    for u, v in ba_directed.edges:
        ba_directed[u][v]['weight'] = random.uniform(1, 100)

    return ba_directed


def save_graph(graph, file_name, folder="graphs"):
    # Creazione della cartella "custom_graphs" se non esiste
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file_name)
    # Salvataggio del grafo in formato pickle
    with open(file_path, 'wb') as f:
        pickle.dump(graph, f)
    print(f"Grafo salvato in {file_path}")


if __name__ == '__main__':
    # nodes = [5000, 10000, 15000, 20000, 25000]
    nodes = [5000, 15000, 25000, 30000]
    # ms = [10, 15, 20, 25, 30]

    for n in nodes:
        graph = generate_graph(n, 5)

        save_graph(graph, f"graph_{n}.pkl")

        with open(f"graphs/graph_{n}.pkl", "rb") as f:
            loaded_graph = pickle.load(f)

        print(f"Grafo {n} nodi")
        print(loaded_graph.number_of_nodes())
        print(loaded_graph.number_of_edges())

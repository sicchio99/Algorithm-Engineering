import networkx as nx
import random
import os
import pickle  # Per la serializzazione del grafo


def create_connected_weighted_graph(num_nodes):
    # Grafo vuoto
    G = nx.Graph()

    G.add_nodes_from(range(num_nodes))

    # Creazione dell'albero per assicurare che il grafo sia connesso
    for i in range(num_nodes - 1):
        weight = random.randint(1, 11)
        G.add_edge(i, i + 1, weight=weight)

    # Aggiunta ulteriori archi casuali per aumentare la densità del grafo
    additional_edges = random.randint(num_nodes, 2 * num_nodes)
    while additional_edges > 0:
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u != v and not G.has_edge(u, v):  # Evita duplicati
            weight = random.randint(1, 10)
            G.add_edge(u, v, weight=weight)
            additional_edges -= 1

    return G


def save_graph(graph, file_name, folder="custom_graphs"):
    # Creazione della cartella "custom_graphs" se non esiste
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file_name)
    # Salvataggio del grafo in formato pickle
    with open(file_path, 'wb') as f:
        pickle.dump(graph, f)
    print(f"Grafo salvato in {file_path}")


if __name__ == '__main__':
    for i in range(1, 6):
        nodes = random.randint(8000, 12000)
        G = create_connected_weighted_graph(nodes)
        save_graph(G, f"graph_test{i}.pkl")

        with open(f"custom_graphs/graph_test{i}.pkl", "rb") as f:
            loaded_graph = pickle.load(f)

        print(f"Grafo {i}")
        print(loaded_graph.number_of_nodes())
        print(loaded_graph.number_of_edges())

import pickle
import networkx as nx
import os


def compute_exact_distances(G):
    """
    Calcola le distanze esatte per i nodi usando l'algoritmo Dijkstra.
    Restituisce un dizionario con i nodi e le distanze calcolate.
    :param G: Grafo da analizzare
    """
    exact_distances = {}
    nodes = list(G.nodes)

    for v in nodes:
        print("Nodo", v)
        # Calcolo dellle distanze da v a tutti gli altri nodi usando Dijkstra
        distances = nx.single_source_dijkstra_path_length(G, v, weight='weight')
        exact_distances[v] = distances

    return exact_distances


def centrality_closeness(G, exact_distances):
    """
    Calcola la closeness centrality e la distanza media per ogni nodo nel grafo.
    :param G: Grafo da analizzare
    :param exact_distances: Dizionario con i nodi e le distanze calcolate
    """
    closeness_centrality = {}
    avg_distances = {}
    n = len(G.nodes)

    for v, distances in exact_distances.items():
        # Somma le distanze a tutti gli altri nodi
        distance_sum = sum(distances.values())
        if distance_sum > 0:  # Per evitare divisioni per zero
            closeness_centrality[v] = (n - 1) / distance_sum
            avg_distances[v] = distance_sum / (n - 1)
        else:
            closeness_centrality[v] = 0  # Se isolato, centralità 0
            avg_distances[v] = float('inf')  # Distanza media infinita

    return closeness_centrality, avg_distances


if __name__ == "__main__":

    with open(f"graphs/graph_2500.pkl", "rb") as f:
        G = pickle.load(f)

    num_nodi = G.number_of_nodes()
    print(f"Il grafo ha {num_nodi} nodi.")
    num_arch = G.number_of_edges()
    print(f"Il grafo ha {num_arch} archi.")

    # Calcolo delle distanze esatte
    exact_distances = compute_exact_distances(G)

    # Calcolo della centralità e delle distanze medie
    closeness_centrality, avg_distances = centrality_closeness(G, exact_distances)

    # Ordinamento dei risultati in base alla centralità decrescente
    sorted_results = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)

    # Creazione della cartella results se non esiste
    output_dir = "exact_results"
    os.makedirs(output_dir, exist_ok=True)

    # Salvataggio dei risultati in un file nella cartella results
    output_file = os.path.join(output_dir, "centrality_results_2500.txt")
    with open(output_file, "w") as f:
        f.write("Nodo\tCentralità\tDistanza Media\n")
        for node, centrality in sorted_results:
            avg_distance = avg_distances[node]
            f.write(f"{node}\t{centrality:.6f}\t{avg_distance:.6f}\n")

    # Stampa del file salvato e dei risultati ordinati
    print(f"Risultati salvati in: {output_file}")

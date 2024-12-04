import networkx as nx
import random


def randAlgorithm(G, k):
    """
    Algoritmo RAND per stimare l'inversa della centralità di tutti i nodi di un grafo.
    """
    centrality_estimates = {node: 0 for node in G.nodes()}
    sampled_nodes = []  # Lista dei nodi campionati
    n = G.number_of_nodes()

    # Esegui k iterazioni per stimare l'inversa della centralità
    for i in range(k):
        # Seleziona un nodo casuale come sorgente
        vi = random.choice(list(G.nodes()))
        sampled_nodes.append(vi)  # Salva il nodo campionato
        # Risolvi il problema del SSSP per il nodo vi
        distances = compute_sssp(G, vi)

        # Aggiorna la stima della centralità per ciascun nodo u
        for u in G.nodes():
            centrality_estimates[u] += (n / (n - 1)) * distances[u] / (k * (n - 1))

    # L'inversa della centralità è la media delle distanze
    inverse_centralities = {u: 1 / estimate if estimate != 0 else float('inf')
                            for u, estimate in centrality_estimates.items()}

    return inverse_centralities, sampled_nodes


def compute_sssp(G, source):
    """
    Calcola le distanze minime da un nodo sorgente a tutti gli altri nodi usando il Single Source Shortest Path (SSSP).
    """
    return nx.single_source_dijkstra_path_length(G, source, weight='weight')

import networkx as nx
import random


def randAlgorithm(G, l):
    """
    Algoritmo RAND per stimare l'inversa della centralità di l nodi di un grafo.
    """
    # centrality_estimates = {}
    sampled_nodes = []  # Lista dei nodi campionati
    n = G.number_of_nodes()
    # Inizializza un accumulatore per le somme delle distanze
    inverse_centrality_estimates = {u: 0 for u in G.nodes()}

    # Esegui k iterazioni per stimare l'inversa della centralità
    for i in range(l):
        print(f"\nIterazione {i + 1}/{l}:")
        # Seleziona un nodo casuale come sorgente
        vi = random.choice(list(G.nodes()))
        sampled_nodes.append(vi)  # Salva il nodo campionato

        # Risolvi il problema del SSSP per il nodo vi
        distances = compute_sssp(G, vi)

        # Aggiorna l'accumulatore delle somme delle distanze
        for u in G.nodes():
            contribution = n * distances[u] / (l * (n - 1))
            inverse_centrality_estimates[u] += contribution  # La distanza media è semplicemente il valore accumulato
            # print(f"    Aggiorno nodo {u}: somma += {contribution:.4f} -> somma attuale = {distance_sums[u]:.4f}")

    # Calcola la centralità per ogni nodo
    # print("\nCalcolo della centralità:")
    # for u in G.nodes():
        # if distance_sums[u] > 0:
            # centrality_estimates[u] = 1/distance_sums[u]
         # else:
            # centrality_estimates[u] = float('inf')  # Caso speciale
        # print(f"  Nodo {u}: centralità = {centrality_estimates[u]:.4f}")

    return inverse_centrality_estimates, sampled_nodes



def compute_sssp(G, source):
    """
    Calcola le distanze minime da un nodo sorgente a tutti gli altri nodi usando il Single Source Shortest Path (SSSP).
    """
    return nx.single_source_dijkstra_path_length(G, source, weight='weight')

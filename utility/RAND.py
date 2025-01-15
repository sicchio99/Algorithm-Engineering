import networkx as nx
import random


def randAlgorithm(G, l):
    """
    Algoritmo RAND per stimare l'inversa della centralità di l nodi di un grafo.
    :param G: Grafo da analizzare
    :param l: numero di campioni da estrarre casualmente dal grafo
    """
    n = G.number_of_nodes()

    # Inizializzazione di un accumulatore per le somme delle distanze
    inverse_centrality_estimates = {u: 0 for u in G.nodes()}

    # Inizializzazione un dizionario per le distanze massime per ogni nodo campionato
    max_distances = {}

    # l iterazioni per stimare l'inversa della centralità
    for i in range(l):

        # Selezione di un nodo casuale come sorgente
        vi = random.choice(list(G.nodes()))

        # Risoluzione del problema SSSP per il nodo vi
        distances = compute_sssp(G, vi)

        # Aggiornamento dell'accumulatore delle somme delle distanze
        for u in G.nodes():
            contribution = n * distances[u] / (l * (n - 1))
            inverse_centrality_estimates[u] += contribution

        # Calcolo della distanza massima per il nodo campionato vi
        max_distances[vi] = max(distances.values())

    return inverse_centrality_estimates, max_distances


def update_centrality_estimates(G, q, inverse_centrality_estimates, max_distances, l):
    """
    Aggiorna le stime delle distanze medie e delle distanze massime
    aggiungendo q nuovi vertici al campionamento, considerando anche le distanze massime precedenti.
    :param G: Grafo da analizzare
    :param q: numero di nuovi vertici da campionare
    :param inverse_centrality_estimates: stime delle distanze medie
    :param max_distances: distanze massime
    :param l: numero di campioni estratti casualmente dal grafo
    """
    n = G.number_of_nodes()

    for _ in range(q):
        # Selezione di un nuovo nodo casuale come sorgente
        vi = random.choice(list(G.nodes()))

        # Calcolo delle distanze da vi a tutti gli altri nodi
        distances = compute_sssp(G, vi)

        # Aggiornamento dell'accumulatore delle somme delle distanze
        for u in G.nodes():
            contribution = n * distances[u] / ((l + q) * (n - 1))
            inverse_centrality_estimates[u] += contribution

        # Aggiornamento della distanza massima considerando i valori precedenti
        max_distances[vi] = max(max_distances.get(vi, 0), max(distances.values()))

    return inverse_centrality_estimates, max_distances


def compute_sssp(G, source):
    """
    Calcola le distanze minime da un nodo sorgente a tutti gli altri nodi usando il Single Source Shortest Path (SSSP).
    :param G: Grafo da analizzare
    :param source: nodo sorgente
    """
    return nx.single_source_dijkstra_path_length(G, source, weight='weight')

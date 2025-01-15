import networkx as nx
import numpy as np
import math


def identify_candidates(G, sorted_vertices, delta, l, k):
    """
    Identifica i candidati (insieme E) sulla base della condizione: 𝑎𝑣 ≤ 𝑎𝑣𝑘 + f(ℓ) ⋅ Δ
    :param G: Grafo da analizzare
    :param sorted_vertices: Lista ordinata di tuple (vertice, distanza media)
    :param delta: Valore di Δ
    :param l: Numero di campioni estratti casualmente dal grafo
    :param k: Numero di vertici da selezionare
    """
    f_l = 1.25 * math.sqrt(math.log(G.number_of_nodes()) / l)  # Funzione f(ℓ)

    # Estrazione della distanza media stimata per v_k (k-esimo vertice)
    a_vk = sorted_vertices[k - 1][1]

    # Calcolo della soglia
    threshold = a_vk + f_l * delta

    # Insieme dei candidati
    candidates = []

    # Selezione dei vertici che soddisfano la condizione
    for v, avg_distance in sorted_vertices:
        if avg_distance <= threshold:
            candidates.append(v)

    return candidates


def compute_exact_distances(G, candidates):
    """
    Calcola le distanze esatte per i candidati in E usando l'algoritmo Dijkstra.
    Restituisce un dizionario con i nodi e le distanze calcolate.
    :param G: Grafo da analizzare
    :param candidates: Insieme di vertici candidati
    """
    exact_distances = {}

    for v in candidates:
        distances = nx.single_source_dijkstra_path_length(G, v, weight='weight')
        exact_distances[v] = distances

    return exact_distances


def select_top_k_vertices(exact_distances, k):
    """
    Seleziona i top k vertici in base alla centralità di vicinanza (inverso della distanza media).
    :param exact_distances: Dizionario con i nodi e le distanze calcolate
    :param k: Numero di vertici da selezionare
    """
    # Creazione lista di tuple (vertice, distanza media)
    vertices_with_distances = []

    for v, distances in exact_distances.items():
        # Calcolo della distanza media per ogni vertice
        avg_distance = np.mean(list(distances.values()))
        vertices_with_distances.append((v, avg_distance))

    # Ordinamento dei vertici in ordine crescente rispetto alla loro distanza media
    sorted_candidates = sorted(vertices_with_distances, key=lambda x: x[1])

    # Selezione dei primi k vertici
    top_k_vertices = sorted_candidates[:k]

    return top_k_vertices
import networkx as nx
import numpy as np
import math


def identify_candidates(G, sorted_vertices, delta, l, k):
    """
    Identifica i candidati (insieme E) sulla base della condizione:
    𝑎𝑣 ≤ 𝑎𝑣𝑘 + 2 ⋅ f(ℓ) ⋅ Δ
    """
    f_l = 1.25 * math.sqrt(math.log(G.number_of_nodes()) / l)  # Funzione f(ℓ). alfa = 1.1, alfa > 1
    #print("f(ℓ) = ", f_l)

    # Estrazione della distanza media stimata per v_k (k-esimo vertice)
    a_vk = sorted_vertices[k - 1][1]

    # Calcolo della soglia
    threshold = a_vk + 1 * f_l * delta  # coeff originale = 2
    #print(f"Soglia per i candidati: {threshold}")

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
    """
    exact_distances = {}

    for v in candidates:
        distances = nx.single_source_dijkstra_path_length(G, v, weight='weight')
        exact_distances[v] = distances

    return exact_distances


def select_top_k_vertices(exact_distances, k):
    """
    Seleziona i top k vertici in base alla distanza esatta dalla centralità di vicinanza.
    Ordinamento dei candidati in base alla loro distanza media esatta.
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
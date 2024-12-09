from datetime import datetime
import networkx as nx
import numpy as np
import RAND as rand
import pickle  # Per la serializzazione del grafo
import math


def Toprank2(G, k):
    """
        Algoritmo euristico di ranking basato sulla closeness centrality dei vertici di un grafo
        :param G: Grafo da analizzare
        :param k: numero dei top k vertici da ottenere
        :return: top k vertici ordinati in base allla closeness centrality
        """
    # Step 1: Ordinamento dei vertici sulla base delle distanze medie stimate.
    # l = numero di campioni estratti casualmente dal grafo
    l = int((G.number_of_nodes() ** (2 / 3)) / (math.log(G.number_of_nodes()) ** (1 / 3)))
    print("L", l)

    # Sorted_vertices è una lista ordinata di tuple (vertex_name, avg_distance)
    sorted_vertices, max_distances = rand_and_order_vertices_by_average_distance(G, l)
    print("Fine esecuzione RAND")

    # Step 2: Calcolo di Δ
    delta = 1 * min(max_distance for max_distance in max_distances.values())  # coeff originale = 2
    print(f"Il valore di Δ è: {delta}")

    # Step 3: Computazione del set di vertici candidati
    candidates = identify_candidates(sorted_vertices, delta, l)
    print(f"Numero di candidati: {len(candidates)}")

    # PARTE NUOVA
    p = len(candidates)
    p_1 = 0
    q = int(math.log(G.number_of_nodes()))
    while (p - p_1) <= q:
        p = len(candidates)
        avg_distances, max_distances = rand.randAlgorithm(G, p)
        # AGGIUNGERE: aggiornare distanze medie stimate precedenti
        l = l + q
        delta = min(delta, 1 * min(max_distance for max_distance in max_distances.values()))
        # Ordinamento dei vertici in base alla distanza media (crescente)
        sorted_vertices = sorted(avg_distances.items(), key=lambda item: item[1])

        candidates = identify_candidates(sorted_vertices, delta, l)
        print(f"Numero di candidati: {len(candidates)}")

        p_1 = len(candidates)
        print(f"(p - p') = ({p} - {p_1}) = {(p-p_1)}")

    print("Fine ciclo")

    # Step X: Calcolo delle distanze esatte per il set di vertici candidati
    print("Calcolo delle distanze esatte per il set di vertici candidati")
    exact_distances = compute_exact_distances(G, candidates)

    # Step Y: Selezione dei Top-k vertici
    top_k_vertices = select_top_k_vertices(exact_distances, k)

    return result



def rand_and_order_vertices_by_average_distance(G, l):
    """
    Ordina i vertici di un grafo in base alla distanza media calcolata usando l'algoritmo di campionamento RAND.
    """
    avg_distances, max_distances = rand.randAlgorithm(G, l)

    # Stampa dei primi 10 risultati come esempio
    #print("Valori non ordinati")
    #for node in list(avg_distances.keys())[:10]:
        #print(f"Node {node}, Estimated Inverse Centrality: {avg_distances[node]}")

    # Ordinamento dei vertici in base alla distanza media (crescente)
    sorted_vertices = sorted(avg_distances.items(), key=lambda item: item[1])
    # print("Sorted vertices")
    # print(sorted_vertices[:10])

    return sorted_vertices, max_distances


def identify_candidates(sorted_vertices, delta, l):
    """
    Identifica i candidati (insieme E) sulla base della condizione:
    𝑎𝑣 ≤ 𝑎𝑣𝑘 + 2 ⋅ f(ℓ) ⋅ Δ
    """
    f_l = 1.1 * math.sqrt(math.log(G.number_of_nodes()) / l)  # Funzione f(ℓ). alfa = 1.1, alfa > 1
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


if '__main__' == __name__:
    with open(f"graphs/graph_test1.pkl", "rb") as f:
        G = pickle.load(f)

    num_nodi = G.number_of_nodes()
    print(f"Il grafo ha {num_nodi} nodi.")
    num_arch = G.number_of_edges()
    print(f"Il grafo ha {num_arch} archi.")

    """
    Aggiungere eventuale visualizzazione del grafo
    """

    k = 10
    print("Valore K:", k)

    print(datetime.now())
    result = Toprank2(G, k)
    print(datetime.now())
    for i, (vertex, avg_distance) in enumerate(result, start=1):
        print(f"v{i}: Nodo originale: {vertex}, Distanza media esatta: {avg_distance}")

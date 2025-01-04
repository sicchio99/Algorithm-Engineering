from datetime import datetime
from utility.RAND import randAlgorithm, update_centrality_estimates
import pickle  # Per la serializzazione del grafo
import math
from utility.utils import identify_candidates, compute_exact_distances, select_top_k_vertices


def Toprank2(G, k):
    """
        Algoritmo euristico di ranking basato sulla closeness centrality dei vertici di un grafo
        :param G: Grafo da analizzare
        :param k: numero dei top k vertici da ottenere
        :return: top k vertici ordinati in base allla closeness centrality
        """
    # Step 1: Ordinamento dei vertici sulla base delle distanze medie stimate.
    l = int((G.number_of_nodes() ** (2 / 3)) / (math.log(G.number_of_nodes()) ** (1 / 3)))
    print("L", l)

    # Sorted_vertices è una lista ordinata di tuple (vertex_name, avg_distance)
    sorted_vertices, max_distances, avg_distances = rand_and_order_vertices_by_average_distance(G, l)
    print("Fine esecuzione RAND")

    # Step 2: Calcolo di Δ
    delta = 2 * min(max_distance for max_distance in max_distances.values())
    print(f"Il valore di Δ è: {delta}")

    # Step 3: Computazione del set di vertici candidati
    candidates = identify_candidates(G, sorted_vertices, delta, l, k)
    print(f"Numero di candidati iniziale: {len(candidates)}")

    # Step 4: Inizio parte iterativa dell'algoritmo
    p = len(candidates)  # Numero vertici candidati
    p_1 = 0  # Numero nuovi vertici candidati
    q = int(math.log(G.number_of_nodes()))  # Numero nuovi vertici estratti casualmente dal grafo
    i = 2
    # print(f"Partenza: (p - p') = ({p} - {p_1}) = {(p - p_1)}")
    while (p - p_1) > q:
        p = len(candidates)
        # print(f"Numero di candidati: {len(candidates)}")
        # print(f"Numero vecchi campioni: {l} - Numero campioni aggiuntivi: {q}")
        # print(f"Inizio Rand {i}")
        # Nuova esecuzione di RAND per aggiornare distanze medie e massime usando i nuovi campioni estratti
        avg_distances, max_distances = update_centrality_estimates(G, q, avg_distances, max_distances, l)
        l = l + q
        # print(f"Nuovo l: {l}")
        # Calcolo del nuovo delta sulla base di quanto ottenuto in RAND
        delta = min(delta, 2 * min(max_distance for max_distance in max_distances.values()))
        # print(f"Nuovo delta: {delta}")
        # Ordinamento dei vertici in base alla distanza media (crescente)
        sorted_vertices = sorted(avg_distances.items(), key=lambda item: item[1])

        # Definizione del nuovo insieme di vertici candidati
        candidates = identify_candidates(G, sorted_vertices, delta, l, k)
        # print(f"Nuovo numero di candidati: {len(candidates)}")

        p_1 = len(candidates)
        # print(f"(p - p') = ({p} - {p_1}) = {(p - p_1)}")
        i = i + 1

    # print("Fine ciclo")

    print(f"Nuovo numero di vertici candidati: {len(candidates)}")

    # Step 5: Calcolo delle distanze esatte per il set di vertici candidati
    print("Calcolo delle distanze esatte per il set di vertici candidati")
    exact_distances = compute_exact_distances(G, candidates)

    # Step 6: Selezione dei Top-k vertici
    top_k_vertices = select_top_k_vertices(exact_distances, k)

    return top_k_vertices


def rand_and_order_vertices_by_average_distance(G, l):
    """
    Ordina i vertici di un grafo in base alla distanza media calcolata usando l'algoritmo di campionamento RAND.
    """
    avg_distances, max_distances = randAlgorithm(G, l)

    # Stampa dei primi 10 risultati come esempio
    # print("Valori non ordinati")
    # for node in list(avg_distances.keys())[:10]:
    # print(f"Node {node}, Estimated Inverse Centrality: {avg_distances[node]}")

    # Ordinamento dei vertici in base alla distanza media (crescente)
    sorted_vertices = sorted(avg_distances.items(), key=lambda item: item[1])
    # print("Sorted vertices")
    # print(sorted_vertices[:10])

    return sorted_vertices, max_distances, avg_distances


if '__main__' == __name__:
    # with open(f"custom_graphs/graph_test1.pkl", "rb") as f:
    with open(f"../graphs/graph_10000.pkl", "rb") as f:
        G = pickle.load(f)

    num_nodi = G.number_of_nodes()
    print(f"Il grafo ha {num_nodi} nodi.")
    num_arch = G.number_of_edges()
    print(f"Il grafo ha {num_arch} archi.")

    k = 10
    print("Valore K:", k)

    start = datetime.now()
    print(f"Start: {start}")
    result = Toprank2(G, k)
    end = datetime.now()
    print(f"Start: {end}")
    for i, (vertex, avg_distance) in enumerate(result, start=1):
        print(f"v{i}: Nodo originale: {vertex}, Distanza media esatta: {avg_distance}")
    duration = end - start
    print(f"Durata Totale: {duration.total_seconds()}")

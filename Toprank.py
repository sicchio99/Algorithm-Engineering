from datetime import datetime
from utility.RAND import randAlgorithm
import pickle  # Per la serializzazione del grafo
import math
from utility.utils import identify_candidates, compute_exact_distances, select_top_k_vertices


def rand_and_order_vertices_by_average_distance(G, l):
    """
    Ordina i vertici di un grafo in base alla distanza media calcolata usando l'algoritmo di campionamento RAND.
    """
    avg_distances, max_distances = randAlgorithm(G, l)

    # Stampa dei primi 10 risultati come esempio
    #print("Valori non ordinati")
    #for node in list(avg_distances.keys())[:10]:
        #print(f"Node {node}, Estimated Inverse Centrality: {avg_distances[node]}")

    # Ordinamento dei vertici in base alla distanza media (crescente)
    sorted_vertices = sorted(avg_distances.items(), key=lambda item: item[1])
    # print("Sorted vertices")
    # print(sorted_vertices[:10])

    return sorted_vertices, max_distances


def Toprank(G, k):
    """
    Algoritmo di ranking basato sulla closeness centrality dei vertici di un grafo
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
    candidates = identify_candidates(G, sorted_vertices, delta, l, k)
    print(f"Numero di candidati: {len(candidates)}")

    # Step 4: Calcolo delle distanze esatte per il set di vertici candidati
    print("Calcolo delle distanze esatte per il set di vertici candidati")
    exact_distances = compute_exact_distances(G, candidates)

    # Step 5: Selezione dei Top-k vertici
    top_k_vertices = select_top_k_vertices(exact_distances, k)

    return top_k_vertices


if __name__ == "__main__":
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

    for j in range(1, 4):
        print(f"ESECUZIONE {j}")
        start = datetime.now()
        result = Toprank(G, k)
        end = datetime.now()
        for i, (vertex, avg_distance) in enumerate(result, start=1):
            print(f"v{i}: Nodo originale: {vertex}, Distanza media esatta: {avg_distance}")
        duration = end - start
        print(f"Durata Totale {j}: {duration.total_seconds()}")

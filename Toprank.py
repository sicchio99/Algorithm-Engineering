from datetime import datetime
import networkx as nx
# import matplotlib.pyplot as plt
import numpy as np
import RAND as rand
import pickle  # Per la serializzazione del grafo
from collections import defaultdict
import math


def rand_and_order_vertices_by_average_distance(G, l):
    """
    Ordina i vertici di un grafo in base alla distanza media calcolata usando l'algoritmo di campionamento RAND.
    """
    # Stima della distanza media (inversa della centralità)
    avg_distances, sampled_nodes, max_distances = rand.randAlgorithm(G, l)
    print(str(len(avg_distances)))

    # Stampa dei primi 10 risultati come esempio
    print("Valori non ordinati")
    for node in list(avg_distances.keys())[:10]:
        print(f"Node {node}, Estimated Inverse Centrality: {avg_distances[node]}")

    # Ordinamento dei vertici in base alla distanza media (crescente)
    sorted_vertices = sorted(avg_distances.items(), key=lambda item: item[1])
    # print("Sorted vertices")
    # print(sorted_vertices[:10])

    return sorted_vertices, sampled_nodes, max_distances


def identify_candidates(sorted_vertices, delta, l):
    """
    Identifica i candidati (insieme E) sulla base della condizione:
    𝑎𝑣 ≤ 𝑎𝑣𝑘 + 2 ⋅ f(ℓ) ⋅ Δ
    """
    f_l = 1.1 * math.sqrt(math.log(G.number_of_nodes()) / l)  # Funzione f(ℓ). alfa = 1.1, alfa > 1
    print("f(ℓ) = ", f_l)
    # Estrai la distanza media stimata per v_k (k-esimo vertice)
    v_k = sorted_vertices[k - 1]  # k-1 perché l'indice inizia da 0
    print(f"Il vertice v_k è: {v_k[0]}, con distanza stimata: {v_k[1]}")
    a_vk = v_k[1]  # La distanza media stimata per il vertice v_k

    # Calcola la soglia
    threshold = a_vk + 1 * f_l * delta # coeff originale = 2
    print(f"Soglia per i candidati: {threshold}")

    # Insieme dei candidati
    candidates = []
    print("I vertici pre-selezione sono:", len(sorted_vertices))

    # Seleziona i vertici che soddisfano la condizione
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
    c = 1

    for v in candidates:
        print(f"Esecuzione candidato {c}/{len(candidates)}")
        # Calcola le distanze da v a tutti gli altri nodi usando Dijkstra
        distances = nx.single_source_dijkstra_path_length(G, v, weight='weight')
        exact_distances[v] = distances
        c+=1

    return exact_distances


def select_top_k_vertices(exact_distances, k):
    """
    Seleziona i top k vertici in base alla distanza esatta dalla centralità di vicinanza.
    Ordinando i candidati in base alla loro distanza media esatta.
    """
    # Crea una lista di tuple (vertice, distanza media)
    vertices_with_distances = []

    for v, distances in exact_distances.items():
        # Calcola la distanza media per ogni vertice
        avg_distance = np.mean(list(distances.values()))
        vertices_with_distances.append((v, avg_distance))

    # Ordina i vertici in ordine crescente rispetto alla loro distanza media
    sorted_candidates = sorted(vertices_with_distances, key=lambda x: x[1])

    # Seleziona i primi k vertici
    top_k_vertices = sorted_candidates[:k]

    return top_k_vertices


def Toprank(G, k):
    # Ordinamento dei vertici sulla base delle distanze medie stimate.
    # l = numero di campioni estratti casualmente dal grafo
    l = int((G.number_of_nodes() ** (2 / 3)) / (math.log(G.number_of_nodes()) ** (1 / 3)))
    # l = 40
    print("L", l)
    # Sorted_vertices è una lista ordinata di tuple (vertex_name, avg_distance)
    sorted_vertices, sampled_nodes, max_distances = rand_and_order_vertices_by_average_distance(G, l)

    # Stampa dei primi 10 vertici ordinati in base alla loro distanza media stimata
    print("Primi k vertici ordinati")
    for index, (vertex, avg_distance) in enumerate(sorted_vertices[:10], start=1):
        print(f"v{index}: Node {vertex}, Estimated Average Distance: {avg_distance}")

    # Calcolo di Δ
    print("Distanze max")
    print(str(max_distances))
    delta = 1 * min(max_distance for max_distance in max_distances.values())  # coeff originale = 2
    print(f"Il valore di Δ è: {delta}")

    # Computazione del set di vertici candidati
    candidates = identify_candidates(sorted_vertices, delta, l)
    print(f"Numero di candidati: {len(candidates)}")
    # print(f"Primi candidati: {candidates[:10]}")

    # Test della funzione Step 6
    exact_distances = compute_exact_distances(G, candidates)

    # Test della funzione Step 7
    top_k_vertices = select_top_k_vertices(exact_distances, k)

    # Output dei risultati
    # print(f"I top {k} vertici selezionati sono:")
    # for i, (vertex, avg_distance) in enumerate(top_k_vertices, start=1):
        # print(f"v{i}: Nodo originale: {vertex}, Distanza media esatta: {avg_distance}")

    return top_k_vertices


with open(f"graphs/graph_test1.pkl", "rb") as f:
    G = pickle.load(f)

num_nodi = G.number_of_nodes()
print(f"Il grafo ha {num_nodi} nodi.")
num_arch = G.number_of_edges()
print(f"Il grafo ha {num_arch} archi.")

"""
# Visualizzazione del grafo e dei pesi
pos = nx.spring_layout(G)  # Posizione dei nodi per la visualizzazione
weights = nx.get_edge_attributes(G, 'weight')  # Ottieni i pesi degli archi

# Disegna il grafo
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels=weights)

# Mostra il grafico
plt.show()
"""

# k = int(np.log2(num_nodi))  # Numero di iterazioni basato su log2(n)
k = 10
print("Valore K:", k)

partial_result = Toprank(G, k)
for i, (vertex, avg_distance) in enumerate(partial_result, start=1):
    print(f"v{i}: Nodo originale: {vertex}, Distanza media esatta: {avg_distance}")
"""
results = []
print(datetime.now())
for i in range(1, 2):
    print("ESECUZIONE", i)
    partial_result = Toprank(G, k)
    for i, (vertex, avg_distance) in enumerate(partial_result, start=1):
        print(f"v{i}: Nodo originale: {vertex}, Distanza media esatta: {avg_distance}")
    results.append(partial_result)
    print(datetime.now())

# Per contare in quanti array appare ogni primo elemento della tupla
presence_count = defaultdict(int)

# Per raccogliere i secondi elementi di ogni primo elemento
second_values = defaultdict(list)

# Analisi degli array
num_arrays = len(results)  # Numero totale di array
for i, top_k_vertices in enumerate(results, start=1):
    seen_in_current_array = set()
    for vertex, avg_distance in top_k_vertices:
        if vertex not in seen_in_current_array:
            presence_count[vertex] += 1
            seen_in_current_array.add(vertex)
        second_values[vertex].append(avg_distance)

# Calcolo delle medie delle distanze
averages = {vertex: np.mean(distances) for vertex, distances in second_values.items()}

# Filtrare gli elementi presenti in tutti gli array
elements_in_all_arrays = {vertex: averages[vertex] for vertex, count in presence_count.items() if count == num_arrays}

# Ordinare per la media delle distanze medie
sorted_elements = sorted(elements_in_all_arrays.items(), key=lambda x: x[1])

# Risultati
print("Elementi presenti in tutti gli array, ordinati per la media delle distanze medie:")
for vertex, avg in sorted_elements:
    print(f"Vertex: {vertex}, Media delle distanze medie: {avg:.2f}")

print(datetime.now())
"""


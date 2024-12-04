import networkx as nx
# import random
# import matplotlib.pyplot as plt
import numpy as np
import Graph_generator as Gg
import RAND as rand


def rename_vertices_by_average_distance(G, k):
    """
    Rinomina i vertici di un grafo in base alla distanza media calcolata usando l'algoritmo di campionamento.
    """
    # Step 1: Stima della distanza media (inversa della centralità)
    # avg_distances, sampled_nodes = estimate_inverse_centrality(G, k)
    avg_distances, sampled_nodes = rand.randAlgorithm(G, k)

    # Stampa i primi 10 risultati come esempio
    for node in list(avg_distances.keys())[:10]:
        print(f"Node {node}, Estimated Inverse Centrality: {avg_distances[node]}")

    # Step 2: Ordina i vertici in base alla distanza media (crescente)
    sorted_vertices = sorted(avg_distances.items(), key=lambda item: item[1])
    print(sorted_vertices[:10])

    # Step 3: Rinominazione dei vertici da v1 a vk
    renamed_vertices = {}
    for i, (vertex, avg_distance) in enumerate(sorted_vertices, start=1):
        renamed_vertices[f"v{i}"] = {'vertex_name': vertex, 'avg_distance': avg_distance}

    return renamed_vertices, sorted_vertices, sampled_nodes  # ritornare sorted_vertices per i calcolo di vk e sampled nodes per il calcolo di delta


def compute_delta_from_sample(G, sampled_nodes):
    """
    Calcola il valore di Δ (minimo della massima distanza tra i nodi campionati e gli altri nodi),
    usando i nodi già campionati nello step 1.
    """
    max_distances = []

    for u in sampled_nodes:
        # Calcola le distanze da u a tutti gli altri nodi
        distances = nx.single_source_dijkstra_path_length(G, u, weight='weight')

        # Trova la distanza massima da u a tutti gli altri nodi
        max_dist = max(distances.values())
        max_distances.append(max_dist)

    # Calcola il minimo delle distanze massime tra tutti i nodi campionati
    min_max_distance = min(max_distances)

    # Moltiplica per 2 per ottenere Δ
    delta = 2 * min_max_distance

    return delta


def identify_candidates(G, sorted_vertices, delta, f_l):
    """
    Identifica i candidati (insieme E) sulla base della condizione:
    𝑎𝑣 ≤ 𝑎𝑣𝑘 + 2 ⋅ f(ℓ) ⋅ Δ
    """
    # Estrai la distanza media stimata per v_k (k-esimo vertice)
    v_k = sorted_vertices[k - 1]  # k-1 perché l'indice inizia da 0
    a_vk = v_k[1]  # La distanza media stimata per il vertice v_k

    # Calcola la soglia
    threshold = a_vk + 2 * f_l * delta
    print(f"Soglia per i candidati: {threshold}")

    # Insieme dei candidati
    candidates = []

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

    for v in candidates:
        # Calcola le distanze da v a tutti gli altri nodi usando Dijkstra
        distances = nx.single_source_dijkstra_path_length(G, v, weight='weight')
        exact_distances[v] = distances

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


num_nodes = 100000
# G = create_connected_weighted_graph(num_nodes)
G = Gg.create_connected_weighted_graph(num_nodes)

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

k = int(np.log2(num_nodes))  # Numero di iterazioni basato su log2(n)
print("Valore K:", k)

# Rinominazione dei vertici
renamed_vertices, sorted_vertices, sampled_nodes = rename_vertices_by_average_distance(G, k)

# Stampa i vertici rinominati con la loro distanza media
for i, (vertex, info) in enumerate(renamed_vertices.items()):
    if i >= 10:  # Limita a 10 elementi
        break
    print(f"{vertex}: Nome originale: {info['vertex_name']}, Distanza media: {info['avg_distance']}")

# sorted_vertices è una lista ordinata di tuple (vertex_name, avg_distance)
vk = sorted_vertices[k - 1]  # k-1 perché l'indice inizia da 0
print(f"Il vertice v_k è: {vk[0]}, con distanza stimata: {vk[1]}")

# Calcolo di Δ
delta = compute_delta_from_sample(G, sampled_nodes)
print(f"Il valore di Δ è: {delta}")

# Test della funzione Step 5
f_l = 1  # Esempio di funzione f(ℓ). Puoi modificarla come preferisci.
# Il parametro f(ℓ) dipende dalla configurazione dell'algoritmo e dalla scelta di ℓ
candidates = identify_candidates(G, sorted_vertices, delta, f_l)
print(f"Numero di candidati: {len(candidates)}")
print(f"Primi candidati: {candidates[:10]}")

# Test della funzione Step 6
exact_distances = compute_exact_distances(G, candidates)
print(f"Calcolate distanze esatte per {len(exact_distances)} candidati.")

# Stampa le distanze per i primi 10 candidati
for candidate in list(exact_distances.keys())[:10]:
    print(f"Candidato {candidate}: Distanze esatte calcolate.")
    # Mostra alcune delle distanze calcolate per ogni candidato
    print(list(exact_distances[candidate].items())[:5])  # Mostra le prime 5 distanze per ciascun candidato

# Test della funzione Step 7
top_k_vertices = select_top_k_vertices(exact_distances, k)
print(f"I top {k} vertici selezionati sono:")

# Output dei risultati
print(f"I top {k} vertici selezionati sono:")
for i, (vertex, avg_distance) in enumerate(top_k_vertices, start=1):
    print(f"v{i}: Nodo originale: {vertex}, Distanza media esatta: {avg_distance}")

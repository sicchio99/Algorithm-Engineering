import networkx as nx
import random
# import matplotlib.pyplot as plt
import numpy as np


def create_connected_weighted_graph(num_nodes):
    # Grafo vuoto
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))

    # Creazione albero per assicurare che il grafo sia connesso
    for i in range(num_nodes - 1):
        weight = random.randint(1, 10)  # Peso casuale agli archi
        G.add_edge(i, i + 1, weight=weight)

    # Aggiunta ulteriori archi casuali per aumentare la densità del grafo
    additional_edges = num_nodes  # numero di archi extra che vogliamo aggiungere
    while additional_edges > 0:
        u = random.randint(0, num_nodes - 1)
        v = random.randint(0, num_nodes - 1)
        if u != v and not G.has_edge(u, v):  # Evitiamo cicli e duplicati
            weight = random.randint(1, 10)
            G.add_edge(u, v, weight=weight)
            additional_edges -= 1

    return G


def compute_sssp(G, source):
    """
    Calcola le distanze minime da un nodo sorgente a tutti gli altri nodi usando il Single Source Shortest Path (SSSP).
    """
    return nx.single_source_dijkstra_path_length(G, source, weight='weight')


def estimate_inverse_centrality(G, k):
    """
    Algoritmo RAND per stimare l'inversa della centralità di tutti i nodi di un grafo.
    """
    n = G.number_of_nodes()
    centrality_estimates = {node: 0 for node in G.nodes()}

    # Esegui k iterazioni per stimare l'inversa della centralità
    for i in range(k):
        # Seleziona un nodo casuale come sorgente
        vi = random.choice(list(G.nodes()))
        # Risolvi il problema del SSSP per il nodo vi
        distances = compute_sssp(G, vi)

        # Aggiorna la stima della centralità per ciascun nodo u
        for u in G.nodes():
            centrality_estimates[u] += (n / (n - 1)) * distances[u] / (k * (n - 1))

    # L'inversa della centralità è la media delle distanze
    inverse_centralities = {u: 1 / estimate if estimate != 0 else float('inf')
                            for u, estimate in centrality_estimates.items()}

    return inverse_centralities


def rename_vertices_by_average_distance(G, k):
    """
    Rinomina i vertici di un grafo in base alla distanza media calcolata usando l'algoritmo di campionamento.
    """
    # Step 1: Stima della distanza media (inversa della centralità)
    avg_distances = estimate_inverse_centrality(G, k)

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

    return renamed_vertices, sorted_vertices  # ritornare sorted_vertices per i calcolo di vk


num_nodes = 100000
G = create_connected_weighted_graph(num_nodes)

num_nodi = G.number_of_nodes()
print(f"Il grafo ha {num_nodi} nodi.")
num_arch = G.number_of_edges()
print(f"Il grafo ha {num_arch} archi.")

"""
# Visualizziamo il grafo e i pesi
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
renamed_vertices, sorted_vertices = rename_vertices_by_average_distance(G, k)

# Stampa i vertici rinominati con la loro distanza media
for i, (vertex, info) in enumerate(renamed_vertices.items()):
    if i >= 10:  # Limita a 10 elementi
        break
    print(f"{vertex}: Nome originale: {info['vertex_name']}, Distanza media: {info['avg_distance']}")

# sorted_vertices è una lista ordinata di tuple (vertex_name, avg_distance)
vk = sorted_vertices[k - 1]  # k-1 perché l'indice inizia da 0
print(f"Il vertice v_k è: {vk[0]}, con distanza stimata: {vk[1]}")



import networkx as nx
import random
import matplotlib.pyplot as plt


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


# Imposta il numero di nodi desiderato
num_nodes = 100000

# Crea il grafo connesso
G = create_connected_weighted_graph(num_nodes)

# Calcola e stampa il numero di nodi nel grafo
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

from Toprank import Toprank
from Toprank2 import Toprank2
import os
import pickle
from datetime import datetime
import matplotlib.pyplot as plt


def calculate_position_difference(result, graph):
    """
    Calcola la differenza di posizione tra i risultati di ranking e il file di centralità.
    :param result: Lista di tuple (vertex, avg_distance) prodotta da Toprank.
    :param graph: Il grafo attuale.
    :return: Somma totale delle differenze di posizione.
    """
    # Nome del file da caricare
    filename = f"centrality_results_{graph.number_of_nodes()}.txt"
    filepath = os.path.join("exact_results", filename)

    # Controlla che il file esista
    if not os.path.exists(filepath):
        print(f"File {filename} non trovato.")
        return None

    # Leggi il file di centralità in una lista ordinata
    centrality_positions = {}
    with open(filepath, "r") as file:
        # Salta l'intestazione
        next(file)
        for position, line in enumerate(file, start=1):
            parts = line.split()  # Divide per spazi o tab
            vertex = int(parts[0])  # Primo valore: Nodo
            centrality_positions[vertex] = position

    # Calcola la differenza di posizione
    total_difference = 0
    for rank, (vertex, _) in enumerate(result, start=1):
        if vertex in centrality_positions:
            file_position = centrality_positions[vertex]
            total_difference += abs(rank - file_position)
        else:
            print(f"Vertex {vertex} non trovato nel file centralità.")

    return total_difference


if __name__ == '__main__':

    exp_start = datetime.now()

    # k_value = [3, 5, 10, 15, 20, 30, 50]
    k_value = [3, 5, 10, 15, 20]
    differences = []
    results = []
    durations = []
    # Step 1: import dei grafi
    graphs = []
    """
    for filename in os.listdir("graphs"):
        # Verifica che il file abbia estensione .pkl
        if filename.endswith(".pkl"):
            file_path = os.path.join("graphs", filename)
            # Carica il grafo e aggiungilo all'array
            with open(file_path, "rb") as f:
                G = pickle.load(f)
                graphs.append(G)
    """
    with open(f"graphs/graph_2500.pkl", "rb") as f:
        G = pickle.load(f)
        graphs.append(G)
    with open(f"graphs/graph_5000.pkl", "rb") as f:
        G = pickle.load(f)
        graphs.append(G)
    with open(f"graphs/graph_10000.pkl", "rb") as f:
        G = pickle.load(f)
        graphs.append(G)

    # Step 2: inizio ciclo (per ogni k e per ogni grafo)
    for k in k_value:
        print("--------------------")
        print(f"Test per k = {k}")
        print("--------------------")
        for graph in graphs:

            # Step 2.1 applicazione degli algoritmi di ranking
            print(f"Test su grafo con n = {graph.number_of_nodes()} e m = {graph.number_of_edges()}")
            print("--------------------")

            # Step 2.1.1: esegui Toprank per grafo g, salva risultato e durata
            print(f"Inizio esecuzione Toprank su grafo con n = {graph.number_of_nodes()}")
            start = datetime.now()
            res_1 = Toprank(graph, k)
            end = datetime.now()
            dur_1 = end - start
            for i, (vertex, avg_distance) in enumerate(res_1, start=1):
                print(f"v{i}: Nodo originale: {vertex}, Distanza media esatta: {avg_distance}")
            print(f"Durata dell'esecuzione di Toprank: {dur_1}")
            print("--------------------")

            # Step 2.1.2: esegui Toprank2 per grafo g, salva risultato e durata
            print(f"Inizio esecuzione Toprank 2 su grafo con n = {graph.number_of_nodes()}")
            start = datetime.now()
            res_2 = Toprank2(graph, k)
            end = datetime.now()
            dur_2 = end - start
            for i, (vertex, avg_distance) in enumerate(res_2, start=1):
                print(f"v{i}: Nodo originale: {vertex}, Distanza media esatta: {avg_distance}")
            print(f"Durata dell'esecuzione di Toprank 2: {dur_2}")
            print("--------------------")

            results.append((k, res_1, res_2))
            durations.append((k, graph.number_of_nodes(), dur_1.total_seconds(), dur_2.total_seconds()))

            # Step 2.2: confronta soluzione 1 e 2 con esatto e determina differenza, salva differenza
            diff_1 = calculate_position_difference(res_1, graph)
            print(f"Somma delle differenze per Toprank: {diff_1}")

            diff_2 = calculate_position_difference(res_2, graph)
            print(f"Somma delle differenze per Toprank 2: {diff_2}")

            differences.append((k, graph.number_of_nodes(), diff_1, diff_2))
            print("--------------------")

    print("DURATE: ", str(durations))
    print("DIFFERENZE: ", str(differences))
    print("--------------------")

    # Step 3: creazione dei grafci
    output_dir = "experiment_results"
    os.makedirs(output_dir, exist_ok=True)

    for k in k_value:
        durations_k = [dur for dur in durations if dur[0] == k]
        x = [dur[1] for dur in durations_k]  # Numero di nodi
        y1 = [dur[2] for dur in durations_k]  # Durata Toprank
        y2 = [dur[3] for dur in durations_k]  # Durata Toprank2

        plt.figure(figsize=(10, 6))
        plt.plot(x, y1, label="Toprank", marker='o')
        plt.plot(x, y2, label="Toprank2", marker='s')
        plt.xlabel("Numero di nodi")
        plt.ylabel("Durata (secondi)")
        plt.title(f"Durate degli algoritmi per k = {k}")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, f"durations_k_{k}.png"))
        plt.show()

        # Step 3.2: Grafico qualità del risultato
        # Filtra le differenze per il valore corrente di k
        differences_k = [diff for diff in differences if diff[0] == k]
        x = [diff[1] for diff in differences_k]  # Numero di nodi
        y1 = [diff[2] for diff in differences_k]  # Differenza Toprank
        y2 = [diff[3] for diff in differences_k]  # Differenza Toprank2

        plt.figure(figsize=(10, 6))
        plt.plot(x, y1, label="Toprank", marker='o')
        plt.plot(x, y2, label="Toprank2", marker='s')
        plt.xlabel("Numero di nodi")
        plt.ylabel("Differenza posizione")
        plt.title(f"Differenze dei risultati per k = {k}")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, f"differences_k_{k}.png"))
        plt.show()

    for graph in graphs:
        # 3.3 Durate degli algoritmi al variare di k
        num_nodes = graph.number_of_nodes()
        durations_graph = [dur for dur in durations if dur[1] == num_nodes]
        x = [dur[0] for dur in durations_graph]  # Valori di k
        y1 = [dur[2] for dur in durations_graph]  # Durata Toprank
        y2 = [dur[3] for dur in durations_graph]  # Durata Toprank2

        plt.figure(figsize=(10, 6))
        plt.plot(x, y1, label="Toprank", marker='o')
        plt.plot(x, y2, label="Toprank2", marker='s')
        plt.xlabel("Valore di k")
        plt.ylabel("Durata (secondi)")
        plt.title(f"Durate degli algoritmi per grafo con {num_nodes} nodi")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, f"durations_nodes_{num_nodes}.png"))
        plt.show()

        # 3.4 Differenze dei risultati al variare di k (nuovo grafico)
        differences_graph = [diff for diff in differences if diff[1] == num_nodes]
        x = [diff[0] for diff in differences_graph]  # Valori di k
        y1 = [diff[2] for diff in differences_graph]  # Differenza Toprank
        y2 = [diff[3] for diff in differences_graph]  # Differenza Toprank2

        plt.figure(figsize=(10, 6))
        plt.plot(x, y1, label="Toprank", marker='o')
        plt.plot(x, y2, label="Toprank2", marker='s')
        plt.xlabel("Valore di k")
        plt.ylabel("Differenza posizione")
        plt.title(f"Differenze dei risultati per grafo con {num_nodes} nodi")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(output_dir, f"differences_nodes_{num_nodes}.png"))
        plt.show()

    exp_end = datetime.now()
    dur_exp = exp_end - exp_start
    print(f"L'esperimento è durato {dur_exp}")

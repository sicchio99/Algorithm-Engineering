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
    filepath = os.path.join("results", filename)  # Assicurati che il percorso sia corretto

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

    k_value = [3, 5, 10, 15, 20, 25, 40, 50]
    differences = []
    results = []
    durations = []
    # Step 1: import dei grafi
    graphs = []
    for filename in os.listdir("graphs"):
        # Verifica che il file abbia estensione .pkl
        if filename.endswith(".pkl"):
            file_path = os.path.join("graphs", filename)
            # Carica il grafo e aggiungilo all'array
            with open(file_path, "rb") as f:
                G = pickle.load(f)
                graphs.append(G)

    # Step 2: inizio ciclo (per ogni k e per ogni grafo)
    for k in k_value:
        print(f"Test per k = {k}")
        for graph in graphs:

            # Step 2.1 applicazione degli algoritmi di ranking
            print(f"Test su grafo con n = {graph.number_of_nodes()} e m = {graph.number_of_edges()}")

            # Step 2.1.1: esegui Toprank per grafo g, salva risultato e durata
            start = datetime.now()
            res_1 = Toprank(graph, k)
            end = datetime.now()
            dur_1 = end - start
            for i, (vertex, avg_distance) in enumerate(res_1, start=1):
                print(f"v{i}: Nodo originale: {vertex}, Distanza media esatta: {avg_distance}")

            # Step 2.1.2: esegui Toprank2 per grafo g, salva risultato e durata
            start = datetime.now()
            res_2 = Toprank2(graph, k)
            end = datetime.now()
            dur_2 = end - start
            for i, (vertex, avg_distance) in enumerate(res_2, start=1):
                print(f"v{i}: Nodo originale: {vertex}, Distanza media esatta: {avg_distance}")

            results.append((k, res_1, res_2))
            durations.append((k, dur_1.total_seconds(), dur_2.total_seconds()))

            # Step 2.2: confronta soluzione 1 e 2 con esatto e determina differenza, salva differenza
            diff_1 = calculate_position_difference(res_1, graph)
            print(f"Somma delle differenze per Toprank: {diff_1}")

            diff_2 = calculate_position_difference(res_2, graph)
            print(f"Somma delle differenze per Toprank: {diff_2}")

            differences.append((k, diff_1, diff_2))

    # Step 3: creazione dei grafci
    for k in k_value:
        # Step 3.1: Grafico prestazioni
        # Filtra le durate per il valore corrente di k
        durations_k = [dur for dur in durations if dur[0] == k]
        x = [graph.number_of_nodes() for graph in graphs]
        y1 = [dur[1] for dur in durations_k]  # Durata Toprank
        y2 = [dur[2] for dur in durations_k]  # Durata Toprank2

        plt.figure(figsize=(10, 6))
        plt.plot(x, y1, label="Toprank", marker='o')
        plt.plot(x, y2, label="Toprank2", marker='s')
        plt.xlabel("Numero di nodi")
        plt.ylabel("Durata (secondi)")
        plt.title(f"Durate degli algoritmi per k = {k}")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"durations_k_{k}.png")  # Salva il grafico come immagine
        plt.show()

        # Step 3.2: Grafico qualità del risultato
        # Filtra le differenze per il valore corrente di k
        differences_k = [diff for diff in differences if diff[0] == k]
        x = [graph.number_of_nodes() for graph in graphs]
        y1 = [diff[1] for diff in differences_k]  # Differenza Toprank
        y2 = [diff[2] for diff in differences_k]  # Differenza Toprank2

        plt.figure(figsize=(10, 6))
        plt.plot(x, y1, label="Toprank", marker='o')
        plt.plot(x, y2, label="Toprank2", marker='s')
        plt.xlabel("Numero di nodi")
        plt.ylabel("Differenza posizione")
        plt.title(f"Differenze dei risultati per k = {k}")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"differences_k_{k}.png")  # Salva il grafico come immagine
        plt.show()


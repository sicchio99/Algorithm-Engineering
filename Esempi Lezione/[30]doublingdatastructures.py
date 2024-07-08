
    
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 17:27:23 2020

@author: anonym
"""

import matplotlib.pyplot as plt
import networkit as nk
import networkx as nx
import sys 
from networkit import graphtools 
import numpy as np
# from random import randrange
# import math
# import random

    
from enum import Enum
def hist2nk(name):
    with open(name, "r", encoding='UTF-8') as fhandle:
        print("READING GRAPH:",name)
        firstline = True
        for line in fhandle:
            # print(line)
            if firstline == True:
                fields = line.split(" ")
                firstline = False
                # print(fields)
                n = int(fields[0])
                m = int(fields[1])
                weighted = int(fields[2])==1
                directed = int(fields[3])==1
                graph = nk.graph.Graph(n,weighted,directed)
            else:
                fields = line.split(" ")
                graph.addEdge(int(fields[1]),int(fields[2]),int(fields[3]))
                    
        if not graph.numberOfEdges()==m:
            print(graph.numberOfEdges(),m)
            raise Exception('misreading of graph')
        wgraph = nk.graph.Graph(graph.numberOfNodes(),graph.isWeighted(),graph.isDirected())
        assert graph.numberOfNodes()==wgraph.numberOfNodes()
        if weighted==True:
            for vertice in range(graph.numberOfNodes()):
                for vicino in graph.iterNeighbors(vertice):
                    wgraph.addEdge(vertice,vicino,graph.weight(vertice,vicino))
        else:
            for vertice in range(graph.numberOfNodes()):
                for vicino in graph.iterNeighbors(vertice):
                    wgraph.addEdge(vertice,vicino)
        return wgraph
class strategy(Enum):
    A = 0
    B = 1

                                
class random_greegy_graph_coloring:
    """A simple example class"""
    
    def __init__(self, g):
        self.uncolored = -1 
        self.graph = g
        self.forbidden_colors = None
        self.check_color_function = None
        self.assign_color_function = None
        self.contatore_istruzioni = 0

        self.colors = [self.uncolored for _ in range(self.graph.numberOfNodes())]
        
                   
    def reset(self,strategy):
        if strategy == strategy.B:
            self.forbidden_colors = [set() for _ in self.graph.iterNodes()]
            self.check_color_function = self.check_color_B
            self.assign_color_function = self.assign_color_B
        else:
            assert strategy == strategy.A
            self.check_color_function = self.check_color_A
            self.assign_color_function = self.assign_color_A
        for vert in self.graph.iterNodes():
            self.colors[vert] = self.uncolored
            
        assert all(self.colors[v]==self.uncolored for v in self.graph.iterNodes())
        self.contatore_istruzioni = 0
    # def is_coloring_done(self):
    #     return self.existsUncoloredVertex()==NULL_VERTEX;
    
    # def existsUncoloredVertex(self):
    #     for i in range(self.graph.numberOfNodes()):
    #         if self.colors[i]==UNCOLORED:
    #             return i;
    #     return NULL_VERTEX;    

    def check_color_A(self,color,vertex):
        for n in self.graph.iterNeighbors(vertex):
            self.contatore_istruzioni+=1
            if self.colors[n]==color:
                assert not all(self.colors[n]!=color for n in self.graph.iterNeighbors(vertex))
                return False
        assert all(self.colors[n]!=color for n in self.graph.iterNeighbors(vertex))
        return True
        
    
    def assign_color_A(self,color,vertex):
        assert self.check_color_A(color,vertex)
        self.colors[vertex]=color
        self.contatore_istruzioni+=1
        
    def check_color_B(self,color,vertex):
        assert self.forbidden_colors[vertex] is not None
        self.contatore_istruzioni+=len(self.forbidden_colors[vertex])
        return color not in self.forbidden_colors[vertex]
    
    def assign_color_B(self,color,vertex):
        assert self.check_color_B(color,vertex)
        self.colors[vertex]=color
        self.contatore_istruzioni+=1
        for n in self.graph.iterNeighbors(vertex):
            self.contatore_istruzioni+=1
            assert self.colors[vertex]!=self.colors[n]
            self.forbidden_colors[n].add(color)

        
    def color_count(self):
        used = set()
        for vert in self.graph.iterNodes():
            if not all(self.colors[vert]!=self.colors[neighbor] for neighbor in self.graph.iterNeighbors(vert)):                
                dbg_list = []
                for neighbor in self.graph.iterNeighbors(vert):
                    dbg_list.append((neighbor,self.colors[neighbor]))
                print(vert,self.colors[vert],dbg_list)
                raise Exception("coloring constraint violated")
            used.add(self.colors[vert]);
        return len(used)
        

    def run_greedy(self,order, strategy):
        
        self.reset(strategy)
        

        
            
        for vertice in order:
            for color in range(self.graph.numberOfNodes()):
                if self.check_color_function(color,vertice):
                    self.assign_color_function(color,vertice);
                    break
        assert all(self.colors[v]!=self.uncolored for v in self.graph.iterNodes())
        return self.color_count(), self.contatore_istruzioni   
     
                
    def run(self, I):
        
        
        assert type(I)==int
        
        bestCount = sys.maxsize #INFTY
        bestPerm = None
        bestColoring = []
        perms = list()
        
        contatore = 0
        instructions_counter_a = []
        instructions_counter_b = []
        
        while contatore<I:
        
            perm = list(np.random.permutation(self.graph.numberOfNodes()))
            perms.append(perm)
            
            color_count_a, instructions_a = self.run_greedy(perm,strategy.A)
            instructions_counter_a.append(instructions_a)
            coloring_a = [(v,self.colors[v]) for v in self.graph.iterNodes()]
            
            
            color_count_b, instructions_b = self.run_greedy(perm,strategy.B)
            instructions_counter_b.append(instructions_b)

            coloring_b = [(v,self.colors[v]) for v in self.graph.iterNodes()]
            
            assert len(coloring_a)==len(coloring_b)
            if color_count_a!=color_count_b:
                raise Exception('the two strategies are not functionally equivalent')
            
            assert all(coloring_a[x]==coloring_b[x] for x in range(len(coloring_a)))
            assert len(instructions_counter_a)==len(instructions_counter_b)

            contatore+=1
            
            if color_count_b < bestCount:
                bestCount = color_count_b
                bestColoring = coloring_b
                bestPerm = perm
                
        return bestColoring, bestCount, bestPerm, perms, instructions_counter_a, instructions_counter_b
    
   
    
    
import argparse  
    
if __name__ == "__main__":
    
    # #GENERAZIONE DI GRAFI
    



    parser = argparse.ArgumentParser()

    parser.add_argument('--t',metavar="TYPE_OF_TEST", type=int, required=True,  help='Tipo di esperimento: [0: time 1: apx]')
    parser.add_argument('--g',metavar="GRAPH", required=True,  help='Path to the graph file (.hist format)')


    args = parser.parse_args()

    tipo = int(args.t)
    if tipo != 0:
        raise Exception('not yet implemented')

    # if ".hist" in str(args.g):
    #     G_prime_prime = hist2nk(str(args.g))
    # elif ".nde" in str(args.g):
    #     G_prime_prime = read_nde(str(args.g))
    # else:    #DOUBLING SU N 
    
    

    # BARA=nk.generators.BarabasiAlbertGenerator(10, 200, n0=0, batagelj=True).generate()
    # print(BARA.numberOfNodes(), BARA.numberOfEdges())
    # G = nx.cycle_graph(4)
    # G = nx.barabasi_albert_graph(40,5)
    graph = hist2nk(str(args.g))
    graph=graphtools.toUndirected(graph)
    graph = graphtools.toUnweighted(graph)    
    graph.removeMultiEdges()
    graph.removeSelfLoops()
    graph.indexEdges()
    
    G_prime = nk.nxadapter.nk2nx(graph)
    if __debug__ and graph.numberOfNodes()<100:
    
        pos = nx.kamada_kawai_layout(G_prime)    
        colori = ['#029386' for _ in range(G_prime.number_of_nodes())]  #'#029386'
        fig, ax = plt.subplots(figsize=(10,10))
        nx.draw(G_prime,pos, node_color=colori,node_size=800,font_size=14)
        nx.draw_networkx_labels(G_prime,pos,font_family="sans-serif",font_size=14)
        ax.set_axis_off()
        fig.tight_layout()
        plt.show()
    
    #algoritmo di riferimento

    d = nx.coloring.greedy_color(G_prime, strategy='largest_first')
    
    
    
    print([value for key,value in d.items()])
    
    used_largest_first = set()
    
    for key,value in d.items():
        used_largest_first.add(value)
        
    print("CHROMATIC NUMBER STATE-OF-THE-ART: ",len(used_largest_first)) 
    
    # graph = nk.nxadapter.nx2nk(G)
    
    iterazioni = 100
    col_graph = random_greegy_graph_coloring(graph)
    best_col,best_count, best_perm, perm_list, I_A, I_B = col_graph.run(I=iterazioni)
    
    print("BEST COLORING: ",best_col)
    print("CHROMATIC NUMBER: ",best_count)
    print("BEST PERM:",best_perm)
    assert len(perm_list)==iterazioni
    assert len(I_A)==iterazioni
    assert len(I_B)==iterazioni
    print(I_A) 
    print(I_B)
    plt.figure(dpi=600)
    plt.plot([i for i in range(iterazioni)],I_A)
    plt.plot([i for i in range(iterazioni)],I_B)
    
    plt.figure(dpi=600)
    plt.plot([i for i in range(iterazioni)],[sum(I_A[0:i]) for i in range(iterazioni)])
    plt.plot([i for i in range(iterazioni)],[sum(I_B[0:i]) for i in range(iterazioni)])

    #per osservare che non c'è dipendenza dalla permutazione
    plt.show()   
    


    
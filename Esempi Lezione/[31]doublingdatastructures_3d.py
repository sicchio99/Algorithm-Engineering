
    
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

from progress.bar import IncrementalBar
   
from enum import Enum

import seaborn as sns

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
        bar = IncrementalBar('Iterations:', max = I)

        while contatore<I:
            bar.next()
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
        bar.finish()
                
        return bestColoring, bestCount, bestPerm, perms, instructions_counter_a, instructions_counter_b
    
   
    
    
import pandas as pd 
import math
if __name__ == "__main__":
    
    
    meta_livelli = 5


    # BARA=nk.generators.BarabasiAlbertGenerator(10, 200, n0=0, batagelj=True).generate()
    # print(BARA.numberOfNodes(), BARA.numberOfEdges())
    # G = nx.cycle_graph(4)
    

    grafi = []

    
    
    n_vertex_set = [25,50,100,200]
    for randoms in [0,1,2]:
        for vertici in n_vertex_set:
            scalature = [vertici,round(3*vertici),round(math.log(vertici)*vertici),round(1/3*(vertici-1)*vertici*0.5),round((vertici-1)*vertici*0.5)]
            meta_livelli = ["sparsest","sparse","medium","dense","full"]
        
            for archi,metal in zip(scalature,meta_livelli):
                assert archi<=round((vertici-1)*vertici*0.5) and archi>0
                grafi.append((nx.gnm_random_graph(vertici,archi),(vertici,archi),metal))

    
   
    grafi = sorted(grafi,key=lambda x: x[1])
    
    """STATS"""
    from datetime import datetime

    import csv
    now = datetime.now() # current date and time
    date_time = now.strftime("%d_%m_%Y_%H_%M_%S")

    statsfile = str("test_"+date_time+'.csv')
    
    measures = ({
    'n':[],
    'm' :[],
    'meta_name' :[],
    'strategy':[],
    'measure':[],
    'ratio':[],
    'better_or_equal_than_A':[]
    })


    misurazioni = pd.DataFrame(measures)
    print("Create DataFrame:\n", misurazioni)
    
    
    with open(statsfile, 'a', newline='', encoding='UTF-8') as csvfile:
        
        writer = csv.writer(csvfile)
        


        writer.writerow(["graphtype",\
                         "date",\
                         "vertices",\
                         "arcs",\
                         "density",\
                         "instructions",\
                        "strategy",\
                         "colors"])
            
    for G,(nodi,archi),metal in grafi:
        
        
        graph = nk.nxadapter.nx2nk(G)
        graph = graphtools.toUndirected(graph)
        graph = graphtools.toUnweighted(graph)    
        graph.removeMultiEdges()
        graph.removeSelfLoops()
        graph.indexEdges()
        
        nk.overview(graph)

        # if __debug__ and graph.numberOfNodes()<200:
        
        #     pos = nx.kamada_kawai_layout(G)    
        #     colori = ['#029386' for _ in range(G.number_of_nodes())]  #'#029386'
        #     fig, ax = plt.subplots(figsize=(10,10))
        #     nx.draw(G,pos, node_color=colori,node_size=800,font_size=14)
        #     nx.draw_networkx_labels(G,pos,font_family="sans-serif",font_size=14)
        #     ax.set_axis_off()
        #     fig.tight_layout()
        #     plt.show()

        
        
        iterazioni = 100 #remove hardcoding
        
        
        col_graph = random_greegy_graph_coloring(graph)
        best_col,best_count, best_perm, perm_list, I_A, I_B = col_graph.run(I=iterazioni)
        
        # print("BEST COLORING: ",best_col)
        # print("CHROMATIC NUMBER: ",best_count)
        # print("BEST PERM:",best_perm)
        assert len(perm_list)==iterazioni
        assert len(I_A)==iterazioni
        assert len(I_B)==iterazioni
        


        assert archi == graph.numberOfEdges()
        with open(statsfile, 'a', newline='', encoding='UTF-8') as csvfile:
            
            writer = csv.writer(csvfile)
            writer.writerow(["gnm",now.strftime("%d_%m_%Y_%H_%M_%S"),graph.numberOfNodes(),graph.numberOfEdges(),round(graph.numberOfEdges()/graph.numberOfNodes(),2),sum(I_A)/iterazioni,"A",best_count])
            writer.writerow(["gnm",now.strftime("%d_%m_%Y_%H_%M_%S"),graph.numberOfNodes(),graph.numberOfEdges(),round(graph.numberOfEdges()/graph.numberOfNodes(),2),sum(I_B)/iterazioni,"B",best_count])                 
        
        
        
        
        new_row = pd.Series({'n':graph.numberOfNodes(),'m':graph.numberOfEdges(),'meta_name':metal,'strategy':"A",'measure':sum(I_A)/iterazioni,'ratio':1.0,'better_or_equal_than_A':True})
        misurazioni=pd.concat([misurazioni, new_row.to_frame().T], ignore_index=True)
        new_row = pd.Series({'n':graph.numberOfNodes(),'m':graph.numberOfEdges(),'meta_name':metal,'strategy':"B",'measure':sum(I_B)/iterazioni,'ratio':sum(I_B)/sum(I_A),'better_or_equal_than_A':True if sum(I_B)<sum(I_A) else False})
        misurazioni=pd.concat([misurazioni, new_row.to_frame().T], ignore_index=True)


        print("After adding new rows to DataFrame:\n", misurazioni)
    
    # assert len(misure_a)==len(misure_b)
    assert len(misurazioni)==len(grafi)*2
    
    
    # grafi = sorted(grafi,key=lambda x: x[1][0])
    

    # sns.set(style = "darkgrid")
    # fig, axs = plt.subplots(nrows=3,figsize=(20, 22))
    sns.set(style='darkgrid')

    plt.figure(dpi=600)
    sns.lineplot( x = "n", y = "measure",hue = "strategy", data = misurazioni)
    plt.figure(dpi=600)
    sns.lineplot( x = "m", y = "measure",hue = "strategy", data = misurazioni)
    plt.figure(dpi=600)
    sns.lineplot( x = "meta_name", y = "ratio",hue = "strategy", data = misurazioni)
    
    plt.figure(dpi=600)
    # If the hue is in numeric format, seaborn will assume that it represents some continuous quantity and will decide to display what it thinks is a representative sample along the color dimension. 
    sns.scatterplot(data = misurazioni[misurazioni['strategy'] =="B"] , x = "m", y = "n", hue = "better_or_equal_than_A")
    # plt.show()   
    # plt.clf()
    # grafi = sorted(grafi,key=lambda x: x[1][1])

    # plt.plot(,misure_a, marker="o")
    # plt.plot([x[1][1] for x in grafi],misure_b, marker="o")
    
    # plt.show()   
    


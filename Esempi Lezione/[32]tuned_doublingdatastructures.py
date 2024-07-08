
    
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
import time
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

        
    def color_count(self,tuned):
        used = set()
        for vert in self.graph.iterNodes():
            assert self.colors[vert]!=self.uncolored or tuned
            if self.colors[vert]!=self.uncolored:
                if not all(self.colors[vert]!=self.colors[neighbor] for neighbor in self.graph.iterNeighbors(vert)):                
                    dbg_list = []
                    for neighbor in self.graph.iterNeighbors(vert):
                        dbg_list.append((neighbor,self.colors[neighbor]))
                    print(vert,self.colors[vert],dbg_list)
                    raise Exception("coloring constraint violated")
            used.add(self.colors[vert]);
        return len(used)
        

    def run_greedy(self,order, strategy, tuned=False,bestcount=-1):
        
        self.reset(strategy)        
            
        for vertice in order:
            for color in range(self.graph.numberOfNodes()):
                if self.check_color_function(color,vertice):
                    self.assign_color_function(color,vertice);
                    if tuned and color>=bestcount:
                        return self.color_count(tuned), self.contatore_istruzioni   

                    break
        assert all(self.colors[v]!=self.uncolored for v in self.graph.iterNodes())
        return self.color_count(tuned), self.contatore_istruzioni   
     
                
    def run(self, I):
        
        
        assert type(I)==int
        
        bestCount = sys.maxsize #INFTY

        perms = list()
        
        
        
        
        bar = IncrementalBar('Gen Permutations:', max = I)
        
        contatore = 0
        while contatore<I:
            bar.next()
            perm = list(np.random.permutation(self.graph.numberOfNodes()))
            perms.append(perm)
            contatore+=1

        assert len(perms)==I
            
        
        untuned_time=time.perf_counter_ns()  
        bar = IncrementalBar('Exec Untuned:', max = I)

        for perm in perms:
            bar.next()

            
            c_count, instr = self.run_greedy(order=perm,strategy=strategy.A,tuned=False,bestcount=-1)

            
            if c_count < bestCount:
                bestCount = c_count
                
        bar.finish()
        untuned_time=time.perf_counter_ns()-untuned_time
        
        tuned_time=time.perf_counter_ns()  
        bar = IncrementalBar('Exec Tuned:', max = I)

        for perm in perms:
            bar.next()            
            c_count, instr = self.run_greedy(order=perm,strategy=strategy.A,tuned=True,bestcount=bestCount)
            
            if c_count < bestCount:
                bestCount = c_count
                
        bar.finish()
        tuned_time=time.perf_counter_ns()-tuned_time
        
        
       
        print("Untuned CPU TIME",untuned_time)
        print("Tuned CPU TIME",tuned_time)
        return untuned_time, tuned_time
    
   
    
    
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
    'tuning_enabled':[],
    'measure':[],
    'ratio':[]
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
                         "time",\
                         "tuning_enabled"])
            
    for G,(nodi,archi),metal in grafi:
        
        
        graph = nk.nxadapter.nx2nk(G)
        graph = graphtools.toUndirected(graph)
        graph = graphtools.toUnweighted(graph)    
        graph.removeMultiEdges()
        graph.removeSelfLoops()
        graph.indexEdges()
        
        nk.overview(graph)


        
        
        iterazioni = 100 #remove hardcoding
        
        
        col_graph = random_greegy_graph_coloring(graph)
        non_tuned_cpu, tuned_cpu = col_graph.run(I=iterazioni)
        



        assert archi == graph.numberOfEdges()
        with open(statsfile, 'a', newline='', encoding='UTF-8') as csvfile:
            
            writer = csv.writer(csvfile)
            writer.writerow(["gnm",now.strftime("%d_%m_%Y_%H_%M_%S"),graph.numberOfNodes(),graph.numberOfEdges(),round(graph.numberOfEdges()/graph.numberOfNodes(),2),non_tuned_cpu,"Tuning",tuned_cpu])
            writer.writerow(["gnm",now.strftime("%d_%m_%Y_%H_%M_%S"),graph.numberOfNodes(),graph.numberOfEdges(),round(graph.numberOfEdges()/graph.numberOfNodes(),2),"No Tuning",non_tuned_cpu])                 
        
        
        
        
        new_row = pd.Series({'n':graph.numberOfNodes(),'m':graph.numberOfEdges(),'meta_name':metal,'tuning_enabled':"Tuning",'measure':tuned_cpu,'ratio':1.0})
        misurazioni=pd.concat([misurazioni, new_row.to_frame().T], ignore_index=True)
        new_row = pd.Series({'n':graph.numberOfNodes(),'m':graph.numberOfEdges(),'meta_name':metal,'tuning_enabled':"No Tuning",'measure':non_tuned_cpu,'ratio':round(non_tuned_cpu/tuned_cpu,2)})
        misurazioni=pd.concat([misurazioni, new_row.to_frame().T], ignore_index=True)


        print("After adding new rows to DataFrame:\n", misurazioni)
    
    assert len(misurazioni)==len(grafi)*2
    
    
    # grafi = sorted(grafi,key=lambda x: x[1][0])
    

    # sns.set(style = "darkgrid")
    # fig, axs = plt.subplots(nrows=3,figsize=(20, 22))
    sns.set(style='darkgrid')

    plt.figure(dpi=600)
    sns.lineplot( x = "n", y = "measure",hue = "tuning_enabled", data = misurazioni)
    plt.figure(dpi=600)
    sns.lineplot( x = "m", y = "measure",hue = "tuning_enabled", data = misurazioni)
    plt.figure(dpi=600)
    sns.lineplot( x = "meta_name", y = "ratio",hue = "tuning_enabled", data = misurazioni)
    



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 01:02:39 2020

@author: anonym
"""
from colored_graph import coloredGraph as cg
from datetime import datetime
from timeit import default_timer as timer
import csv
import auxiliary
from progress.bar import IncrementalBar
import argparse
# import math

NAME={}
NAME[0]='RND'
NAME[1]='AP1'
NAME[2]='AP3'
NAME[3]='LLL'
NAME[4]='ADY'
NAME[5]='ALL'
NAME[6]='DYN'
NAME[7]='1V3'

NULL_EPSILON = -1

CODE={}
CODE['RND']=0
CODE['AP1']=1
CODE['AP3']=2
CODE['LLL']=3
CODE['ADY']=4
CODE['ALL']=5
CODE['DYN']=6
CODE['1V3']=7



if __name__ == "__main__":
    
    helpstring = "";
    
    for k,v in NAME.items():
        helpstring += "#"+str(CODE[v])+" for "+v+"\n";


    NOISE_ITERS = 5;    
    parser = argparse.ArgumentParser(description='KColoring Nash',add_help=True)  
    parser.add_argument("--g",metavar="GRAPH_NAME", required=True, default="", help="path to input graph")
    parser.add_argument("--a",metavar="ALGO_TO_TEST", required=True, default=0,help=helpstring)
    parser.add_argument("--k",metavar="NUM_KOLORS", required=False, default=3,help="Number of colors to use, default=3")
    parser.add_argument("--i",metavar="NUM_DYN_ITERS", required=False, default=1, help="Number of iterations to use for dynamics estimation, default=1")
    parser.add_argument("--e",metavar="EPSILON",required=False, default=2,help="Epsilon for APPROX-3, default=0.2")
    
    
    args = parser.parse_args()
    
    if int(args.a) not in  range(8):
        parser.print_help();
        raise Exception('ALGO_TO_TEST out of range')
        
    KOLORS = int(args.k)
    EPSILON = float(args.e)
    ITERATIONS = int(args.i);

    if KOLORS < 3:
        parser.print_help();
        raise Exception('KOLORS < 3')
        
    if int(args.a)==CODE['AP3']: 
        print("WARNING - GIVEN K IGNORED, WILL BE COMPUTED")
    
      
    if int(args.a)!=CODE['AP3']: 
        print("WARNING - GIVEN EPSILON IGNORED")
        
    if int(args.a)!=CODE['DYN']: 
        print("WARNING - GIVEN ITERATIONS IGNORED")
        ITERATIONS=1
    
    if ITERATIONS < 1:
        parser.print_help();
        raise Exception('ITERATIONS < 1')

    if int(args.a)==CODE['DYN']: 
        if ITERATIONS == 1:
             raise Exception("DYN w SINGLE ITERATION")
        
    print("READING GRAPH: "+str(args.g))
    graph_name = str(args.g)
    graph = auxiliary.hist2nk(graph_name)
    
    if  graph.isDirected()==False:
        raise Exception('UNDIRECTED GRAPH!')
    
    
    print("KOLORS: "+str(KOLORS))
    # graph features 
    print("VERTICES: "+str(graph.numberOfNodes()), "ARCS: "+str(graph.numberOfEdges()))
    print("DIRECTED: "+str(graph.isDirected()))
    print("WEIGHTED: "+str(graph.isWeighted()))
    print("EXPERIMENT TYPE:",str(NAME[int(args.a)]))
     
    # col_graph = cg.coloredGraph(g=graph, kolors=[j for j in range(KOLORS)], another_colored_graph=None)
    col_graph = cg(g=graph, kolors=[j for j in range(KOLORS)])

    
    print("STARTING # COLORS:",str(len(col_graph.getAvailable())))
    UPPERBOUND_ITERATIONS = graph.numberOfNodes()*KOLORS

    if int(args.a)==CODE['RND']: #random coloring
    
        print("== RANDOM COLORING ==")    
        if NAME[int(args.a)]!=NAME[CODE['RND']]:
             raise Exception('wrong algo name')
             
        cpu=timer();
        col_graph.randomColoring();
        elapsed=timer()-cpu 
        if col_graph.colored()==False:
            raise Exception('Non fully colored graph')
        auxiliary.dumpOneShotData(graph_name,col_graph,elapsed,ITERATIONS,str(KOLORS),NAME[int(args.a)],NULL_EPSILON)
        if col_graph.numberOfUsedColors() > KOLORS:
            raise Exception('Anomalous usage of KOLORS')
        
    elif int(args.a)==CODE['AP1']: #Approx1 Coloring 
    
        print("== APPROX1 COLORING ==")
        if NAME[int(args.a)]!=NAME[CODE['AP1']]:
             raise Exception('wrong algo name')
        cpu=timer();
        col_graph.Approx1();
        elapsed=timer()-cpu 
        if col_graph.colored()==False:
            raise Exception('Non fully colored graph')
        auxiliary.dumpOneShotData(graph_name,col_graph,elapsed,ITERATIONS,str(KOLORS),NAME[int(args.a)],NULL_EPSILON)
        
        if col_graph.numberOfUsedColors() > KOLORS:
            raise Exception('Anomalous usage of KOLORS')
            
    elif int(args.a)==CODE['AP3']: #Approx3 Coloring 
        if NAME[int(args.a)]!=NAME[CODE['AP3']]:
            raise Exception('wrong algo name')
        print("== APPROX3 COLORING ==")
        col_graph.setAvailable([j for j in range(int(col_graph.getGraph().numberOfNodes()))])
        print("== RESETTING GIVEN COLORS TO: "+str(len(col_graph.getAvailable())))
        print("== EPSILON: "+str(EPSILON))
        if EPSILON<=0.0:
            raise Exception('epsilon out of range')
        cpu=timer();
        col_graph.Approx3(EPSILON);
        elapsed=timer()-cpu 
        if col_graph.colored()==False:
            raise Exception('Non fully colored graph')
        auxiliary.dumpOneShotData(graph_name,col_graph,elapsed,ITERATIONS,str(len(col_graph.getAvailable())),NAME[int(args.a)],EPSILON)
    
    elif int(args.a)==CODE['ADY']: #DYN_ALGO Coloring, executes dynamics for number_of_nodes*k iterations
        
        if NAME[int(args.a)]!=NAME[CODE['ADY']]:
            raise Exception('wrong algo name')
        print("== DYN_ALGO COLORING ==")    
        
        cpu=timer();
        # UPPERBOUND_ITERATIONS = col_graph.getGraph().numberOfNodes()*int(KOLORS)
        # UPPERBOUND_ITERATIONS =  col_graph.getGraph().numberOfNodes()

        bar = IncrementalBar('Iterations:', max = UPPERBOUND_ITERATIONS)
        
        col_graph.randomColoring();
        
        isnashboolean, gammavalue,fractionvalue = col_graph.nashStatus()
        
        itrs = 1;
        bar.next()

        while itrs < UPPERBOUND_ITERATIONS and isnashboolean==False:
            #evolve
            col_graph.improve()
            isnashboolean, gammavalue,fractionvalue = col_graph.nashStatus()
            bar.next()
            itrs+=1;    


        elapsed=timer()-cpu 

        bar.finish()
        if col_graph.colored()==False:
            raise Exception('Non fully colored graph')
        if col_graph.numberOfUsedColors() > KOLORS:
            raise Exception('Anomalous usage of KOLORS')

            
            
        auxiliary.dumpOneShotData(graph_name,col_graph,elapsed,UPPERBOUND_ITERATIONS,str(KOLORS),NAME[int(args.a)],NULL_EPSILON)

    
    elif int(args.a)==CODE['ALL']:
        avgdeg = sum([col_graph.getGraph().degreeOut(i) for i in range(col_graph.getGraph().numberOfNodes())])/col_graph.getGraph().numberOfNodes()
        maxdeg = max([col_graph.getGraph().degreeOut(i) for i in range(col_graph.getGraph().numberOfNodes())])

        now = datetime.now() # current date and time
        date_time = now.strftime("%d_%m_%Y_%H_%M_%S_%f")
        statsfile = graph_name+"_"+NAME[CODE['ALL']]+"_"+date_time+'.csv';
        auxiliary.headermulti(statsfile)
        cpu=timer();
        with open(statsfile, 'a', newline='') as csvfile:

            
            print("== RANDOM COLORING ==")  
            for iteration in range(NOISE_ITERS):    #to reduce noise due to randomness 
                col_graph.reset()
                cpu=timer();
                col_graph.randomColoring();
                elapsed=timer()-cpu 
                if col_graph.colored()==False:
                    raise Exception('Non fully colored graph')
                if col_graph.numberOfUsedColors() > KOLORS:
                    raise Exception('Anomalous usage of KOLORS')
                isnashboolean, gammavalue,fractionvalue = col_graph.nashStatus()
                auxiliary.dumpMultiData(csvfile,graph_name,col_graph,elapsed,ITERATIONS,str(KOLORS),NAME[CODE['RND']],NULL_EPSILON,avgdeg,maxdeg,isnashboolean, gammavalue,fractionvalue)
                
            print("== APPROX1 COLORING ==")    
            col_graph.reset()
            cpu=timer();
            col_graph.Approx1()
            elapsed=timer()-cpu 
            if col_graph.colored()==False:
                raise Exception('Non fully colored graph')
            if col_graph.numberOfUsedColors() > KOLORS:
                raise Exception('Anomalous usage of KOLORS')
            isnashboolean, gammavalue,fractionvalue = col_graph.nashStatus()
            auxiliary.dumpMultiData(csvfile,graph_name,col_graph,elapsed,ITERATIONS,str(KOLORS),NAME[CODE['AP1']],NULL_EPSILON,avgdeg,maxdeg,isnashboolean, gammavalue,fractionvalue)
           
            print("== LLL RANDOM COLORING ==")  
            for iteration in range(NOISE_ITERS):    #to reduce noise due to randomness 
                col_graph.reset()
                cpu=timer();
                
                # UPPERBOUND_ITERATIONS = round(math.sqrt(col_graph.getGraph().numberOfNodes()),None)
                
                col_graph.LLLColoring(UPPERBOUND_ITERATIONS);
                elapsed=timer()-cpu 
               
                if col_graph.colored()==False:
                    raise Exception('Non fully colored graph')
                if col_graph.numberOfUsedColors() > KOLORS:
                    raise Exception('Anomalous usage of KOLORS')
                isnashboolean, gammavalue,fractionvalue = col_graph.nashStatus()
                auxiliary.dumpMultiData(csvfile,graph_name,col_graph,elapsed,UPPERBOUND_ITERATIONS,str(KOLORS),NAME[CODE['LLL']],NULL_EPSILON,avgdeg,maxdeg,isnashboolean, gammavalue,fractionvalue)
       
            print("== DYN_ALGO COLORING ==")  
            for iteration in range(NOISE_ITERS):    #to reduce noise due to randomness 

                col_graph.reset()
                cpu=timer();
                
                # UPPERBOUND_ITERATIONS = round(math.sqrt(col_graph.getGraph().numberOfNodes()),None)
                # UPPERBOUND_ITERATIONS =  col_graph.getGraph().numberOfNodes()
                bar = IncrementalBar('Iterations:', max = UPPERBOUND_ITERATIONS)
    
                col_graph.randomColoring()
                isnashboolean, gammavalue,fractionvalue = col_graph.nashStatus()
    
                itrs = 1;
                bar.next()
                while itrs < UPPERBOUND_ITERATIONS and isnashboolean==False:
                    #evolve
                    col_graph.improve()
                    isnashboolean, gammavalue,fractionvalue = col_graph.nashStatus()
                    bar.next()
                    itrs+=1;    
                    
                elapsed=timer()-cpu 
    
                bar.finish()
                if col_graph.colored()==False:
                    raise Exception('Non fully colored graph')
                if col_graph.numberOfUsedColors() > KOLORS:
                    raise Exception('Anomalous usage of KOLORS')
                auxiliary.dumpMultiData(csvfile,graph_name,col_graph,elapsed,UPPERBOUND_ITERATIONS,str(KOLORS),NAME[CODE['ADY']],NULL_EPSILON,avgdeg,maxdeg,isnashboolean, gammavalue,fractionvalue)
       
            
        with open(statsfile, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
               print(row)
               
    elif int(args.a)==CODE['DYN']:
        
        bar = IncrementalBar('Iterations:', max = ITERATIONS)


        avgdeg = sum([col_graph.getGraph().degreeOut(i) for i in range(col_graph.getGraph().numberOfNodes())])/col_graph.getGraph().numberOfNodes()
        maxdeg = max([col_graph.getGraph().degreeOut(i) for i in range(col_graph.getGraph().numberOfNodes())])

        print("== DYNAMICS ==")    
        print("== ITERATIONS ==",ITERATIONS)    
        now = datetime.now() # current date and time
        date_time = now.strftime("%d_%m_%Y_%H_%M_%S_%f")
        if NAME[int(args.a)]!=NAME[CODE['DYN']]:
             raise Exception('wrong algo name')
        statsfile = graph_name+"_"+NAME[CODE['DYN']]+"_"+str(KOLORS)+"_"+date_time+'.csv';
        auxiliary.headermulti(statsfile)

       
        cpu=timer();
        with open(statsfile, 'a', newline='') as csvfile:
            #start by random coloring
            col_graph.randomColoring()
            isnashboolean, gammavalue,fractionvalue = col_graph.nashStatus()
            itrs = 0;
            elapsed=timer()-cpu 
            auxiliary.dumpMultiData(csvfile,graph_name,col_graph,elapsed,itrs,str(KOLORS),NAME[CODE['DYN']],NULL_EPSILON,avgdeg,maxdeg,isnashboolean, gammavalue,fractionvalue)
            itrs+=1;
            bar.next()
            while itrs < ITERATIONS and isnashboolean==False:
                #evolve
                col_graph.improve()
                isnashboolean, gammavalue,fractionvalue = col_graph.nashStatus()
                
                elapsed=timer()-cpu 
                auxiliary.dumpMultiData(csvfile,graph_name,col_graph,elapsed,itrs,str(KOLORS),NAME[CODE['DYN']],NULL_EPSILON,avgdeg,maxdeg,isnashboolean, gammavalue,fractionvalue)
                itrs+=1;
                bar.next()

            
            bar.finish()

            if col_graph.colored()==False:
                raise Exception('Non fully colored graph')
            if col_graph.numberOfUsedColors() > KOLORS:
                raise Exception('Anomalous usage of KOLORS')
            print("== IS NASH ==",isnashboolean)    
            print("== GAMMA ==",gammavalue) 
            
    elif int(args.a)==CODE['1V3']:
        avgdeg = sum([col_graph.getGraph().degreeOut(i) for i in range(col_graph.getGraph().numberOfNodes())])/col_graph.getGraph().numberOfNodes()
        maxdeg = max([col_graph.getGraph().degreeOut(i) for i in range(col_graph.getGraph().numberOfNodes())])

        print("== FIRST STEP APPROX3 COLORING ==")
        col_graph.setAvailable([j for j in range(int(col_graph.getGraph().numberOfNodes()))])
        print("== RESETTING GIVEN COLORS TO: "+str(len(col_graph.getAvailable())))
        print("== EPSILON: "+str(EPSILON))
                
        now = datetime.now() # current date and time
        date_time = now.strftime("%d_%m_%Y_%H_%M_%S_%f")
        statsfile = graph_name+"_"+NAME[CODE['1V3']]+"_"+date_time+'.csv';
        auxiliary.headermulti(statsfile)   
        if EPSILON<=0.0:
            raise Exception('epsilon out of range')
        with open(statsfile, 'a', newline='') as csvfile:
            cpu=timer();
            col_graph.Approx3(EPSILON);
            elapsed=timer()-cpu 
            if col_graph.colored()==False:
                raise Exception('Non fully colored graph')
            isnashboolean, gammavalue,fractionvalue = col_graph.nashStatus()
            
            auxiliary.dumpMultiData(csvfile,graph_name,col_graph,elapsed,ITERATIONS,str(len(col_graph.getAvailable())),NAME[CODE['AP3']],EPSILON,avgdeg,maxdeg,isnashboolean, gammavalue,fractionvalue)
    
            k_for_ap1 = col_graph.numberOfUsedColors();    
            print("== SECOND STEP APPROX1 COLORING ==")
    
            print("== RESETTING GIVEN COLORS TO THOSE USED BY AP3: "+str(k_for_ap1))
            col_graph.setAvailable([j for j in range(k_for_ap1)])
            col_graph.reset()
    
            cpu=timer();
            col_graph.Approx1()
            elapsed=timer()-cpu 
            if col_graph.colored()==False:
                raise Exception('Non fully colored graph') 
            if k_for_ap1<col_graph.numberOfUsedColors():
                print(k_for_ap1,col_graph.numberOfUsedColors())
                raise Exception('Anomalous usage of k_for_ap1')
            isnashboolean, gammavalue,fractionvalue = col_graph.nashStatus()
            auxiliary.dumpMultiData(csvfile,graph_name,col_graph,elapsed,ITERATIONS,str(k_for_ap1),NAME[CODE['AP1']],EPSILON,avgdeg,maxdeg,isnashboolean, gammavalue,fractionvalue)
               
        
    else:    
        assert int(args.a)==CODE['LLL']      
        if NAME[int(args.a)]!=NAME[CODE['LLL']]:
            raise Exception('wrong algo name')
        print("== LLL COLORING ==")    
        cpu=timer();
        # UPPERBOUND_ITERATIONS = round(math.sqrt(col_graph.getGraph().numberOfNodes()),None)
        # UPPERBOUND_ITERATIONS =  col_graph.getGraph().numberOfNodes()

        col_graph.LLLColoring(UPPERBOUND_ITERATIONS);
        elapsed=timer()-cpu 
        if col_graph.colored()==False:
            raise Exception('Non fully colored graph')
        auxiliary.dumpOneShotData(graph_name,col_graph,elapsed,UPPERBOUND_ITERATIONS,str(KOLORS),NAME[int(args.a)],NULL_EPSILON)
 
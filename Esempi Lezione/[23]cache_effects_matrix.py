#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 10:59:07 2020

@author: anonym
"""

from random import randrange
import argparse

def generate(n):
    maxV = 10000;
    A = []
    B = []    
  
    for i in range(n):
        A.append([])
        B.append([])
        for j in range(n):    
            A[i].append(randrange(maxV))
            B[i].append(randrange(maxV))
        
    
    return A,B

def scan(A,B,rowwise):   
    if rowwise:
        print("ROW WISE SCAN")
        for i in range(len(A)):
            value = 0
            for j in range(len(A[i])):    
                value+=A[i][j]*B[i][j]  
          
    
    else:
        print("COLUMN WISE SCAN")
        for j in range(len(A)):
            value = 0
            for i in range(len(A[j])):
                value+=A[i][j]*B[i][j]

# import sys
# import numpy as np
import time
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Matrix Sum')
    
    parser.add_argument('--e',metavar="EXPONENT", required=True,  help='Max Size Exponent [Default: 4]', default=4)


    args = parser.parse_args()
    exponent = int(args.e)
    print("exponent:",exponent)
    
    
    if exponent<2:
        exponent=2
        
    matrici_A = []
    matrici_B = []
    
    for n in range(1,exponent):
        
        print("Generating two squared matrices of size:",pow(2,n),"x",pow(2,n))
        
        A,B=generate(pow(2,n))
        matrici_A.append(A)
        matrici_B.append(B)

    print("ROWWISE PROCESSING")        
    
    cpu=time.perf_counter_ns()
    
    for A,B in zip(matrici_A,matrici_B):
        
        scan(A,B,rowwise=True)
        
    rowtime=time.perf_counter_ns()-cpu
    
    print("COLUMNWISE PROCESSING")        


    cpu=time.perf_counter_ns()

    for A,B in zip(matrici_A,matrici_B):

        scan(A,B,rowwise=False)
    
    columntime=time.perf_counter_ns()-cpu
        
    print("ROW-TIME:",(rowtime),"COLUMN-TIME:",(columntime),"RATIO:",round(rowtime/columntime,2))

        
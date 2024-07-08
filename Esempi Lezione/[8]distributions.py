#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 08:44:49 2020

@author: anonym
"""

from numpy import random
import seaborn as sns
#USEFUL
from collections import Counter
import matplotlib.pyplot as plt

        

# Driver code 
if __name__ == "__main__":


    sns.distplot(random.binomial(n=10, p=0.5, size=1000), hist=True, kde=False)
    plt.show() 


    sns.distplot(random.normal(loc=50, scale=5, size=1000), hist=False, label='normal')
    sns.distplot(random.binomial(n=100, p=0.5, size=1000), hist=False, label='binomial')
    
    #POISSON
    #It estimates how many times an event can happen in a specified time. e.g. If someone eats twice a day what is probability he will eat thrice?
    #It has two parameters:
    #lam - rate or known number of occurences e.g. 2 for above problem.
    #size - The shape of the returned array.
    sns.distplot(random.poisson(lam=50, size=1000), hist=False, label='poisson')
    sns.distplot(random.uniform(low=20,high=80,size=1000), hist=False, label='uniform')
    plt.show() 
    # #LOOPKUP
    
    
    EVENTS=["WIN","LOSE","TIE"]
    
    P = [0.45,0.35,0.2]
    prob=[]
    OUTC=[]
    for k in range(len(P)):
        prob.append(sum([P[i] for i in range(k+1)]))
    print(P)
    print(prob)
    
    for i in range(10000):
        r = random.random()
        for p in prob:
            if r<p:
                OUTC.append(EVENTS[prob.index(p)])
                break;
    print(OUTC)
    print(Counter(OUTC))    
    for i,j in zip(Counter(OUTC),Counter(OUTC).values()):
        print(i,j)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 08:20:03 2020

@author: anonym
"""

from numpy import random

# import seaborn as sns

#USEFUL
from collections import Counter
import matplotlib.pyplot as plt

def Bernoulli(A,B,p):
    if random.random()<p:
        return A
    else:
        return B
        
#HARD CODING        
TRIALS=10
PROB=0.1
# Driver code 
if __name__ == "__main__":
    a="HEAD"
    b="TAIL"
    #BIASED COIN TOSS
    OUTCOMES = [Bernoulli(a,b,PROB) for t in range(TRIALS)]
    
    print(OUTCOMES)
    print(Counter(OUTCOMES))
    print(Counter(OUTCOMES).values())
    
    plt.bar(range(len(Counter(OUTCOMES).keys())),Counter(OUTCOMES).values())    
   
    plt.show()
    


# sns.distplot(random.binomial(n=10, p=0.5, size=1000), hist=True, kde=False)

# plt.show() 
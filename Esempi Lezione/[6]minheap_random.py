#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 13:16:00 2020

@author: anonym
"""



m = 2**32;
b = 12345;
a = 1103515245;

# a-1 multiple of 4 since m multiple of 4
# a-1 is divisible by all prime factors of m
# b and m relatively prime


def rng(M=m, A=a, B=b):
    rng.current = (A*rng.current + B) % M
    return rng.current


import time



# Driver Code 
if __name__ == "__main__": 
    # setting the seed
    # rng.current = 1
    rng.current = int(round(time.time() * 1000))
    l = 50;#HARDCODED NO
    #vector of random floats
    
    data = [round(rng(m)/m,2) for i in range(l)];
    
    # Python3 implementation of Min Heap 


    from heapq import heappush, heappop
    
    heap = []
    
    for item in data:
        heappush(heap, item)
    ordered = []
    while heap:
       ordered.append(heappop(heap))
       
    print(ordered)
    print(sorted(data))
    assert ordered == sorted(data)

#EXERCISE IMPLEMENT OTHER GENERATORS
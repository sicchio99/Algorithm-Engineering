#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 09:30:38 2020

@author: anonym
"""

from random import randrange
import matplotlib.pyplot as plt

# WARNING: SHOW INSTALLATION OF PACKAGES VIA APT or PIP3

# Function to do insertion sort 

def insertionSort(arr): 
    # Traverse through 1 to len(arr) 
    """CONTATORE"""
    counter=0;
    for i in range(1, len(arr)): 
  
        
        key = arr[i] 
  
        # Move elements of arr[0..i-1], that are 
        # greater than key, to one position ahead 
        # of their current position 
        j = i-1
        counter+=2;

        while j >=0 and key < arr[j] : 
            arr[j+1] = arr[j] 
            j -= 1
            counter+=2;
        arr[j+1] = key 
        counter+=1;
    # print(round(counter/len(arr),3))
    # return round(counter/len(arr),3);
    print("n:",len(arr),"OPS:",counter,"OPS/n2:",round(counter/(len(arr)*len(arr)),2))
    return counter,round(counter/(len(arr)*len(arr)),2);



if __name__ == "__main__":
    
    n=[]
    contatori=[]
    ratios=[]
    for iterations in range(4,12):
        for attempts in range(3):
            A=[]
            B=[]
            l=pow(2,iterations+1)
            
            while len(A)<l:
                A.append(randrange(pow(2,iterations+1)))
            # print(A[:10])
            # print(A)
            n.append(len(A))
            # print(A)
            B=(sorted(A)).copy()     
            x,y = insertionSort(A)
            
            contatori.append(x)
            ratios.append(y)
            # print(A)
            # print(B)
            assert A == B
    # print(n)
    # print(timers)
    plt.figure(dpi=600)
    plt.plot(n,contatori,"-b", label='counter')
    plt.legend(loc="upper left")
    # The average case running time of an insertion sort algorithm is O(n^2). 
    plt.figure(dpi=600)
    plt.plot(n,ratios,"-r", label='divided_by_n2')
    plt.legend(loc="upper left")
    plt.show()   
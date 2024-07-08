#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 07:47:43 2020

@author: anonym
"""

# Python3 implementation of the 
# above approach 

# import random module 
import random 
from random import randrange
# Function to return the next 
# random number 
def getNum(v): 

	# Size of the vector 
	n = len(v) 

	# Generate a random number within 
	# the index range 
	index = random.randint(0, n - 1) 

	# Get random number from the vector 
	num = v[index] 

	# Remove the number from the vector 
	v[index], v[n - 1] = v[n - 1], v[index] 
	v.pop() 

	# Return the removed number 
	return num 

# Function to generate n non-repeating 
# random numbers 
def generateRandom(n): 
    v = [0] * n 
   
   	# Fill the vector with the values 
   	# 1, 2, 3, ..., n 
    for i in range(n): 
           v[i] = i + 1
   
   	# While vector has elements get a 
   	# random number from the vector 
   	# and print it 
    # print(getNum(v), end = " ") 
    A=[]
    
    while (len(v)) : 
        A.append(getNum(v))
    return A


import math
# Driver code 
if __name__ == "__main__":
    n = 8
    # print(n)
    T = [i for i in generateRandom(n)]
    print(T)
    #some predefined from python
    random.shuffle(T)
    print(T)
    #some predefined from python
    print("RANDOM INTEGER:",randrange(n))
    print("RANDOM FLOAT <=n:",random.random()*n)
    print("RANDOM INTEGER OF T:",random.choice(T))
    #Returns a Python integer with k random bits
    print(pow(2,math.ceil(math.log2(n))))
    print(math.ceil(math.log2(n)))
    
    assert pow(2,math.ceil(math.log2(n)))<=n 
    
    print("RANDOM INTEGER:",random.getrandbits(math.ceil(math.log2(n))))
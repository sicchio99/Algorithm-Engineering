#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 09:21:12 2020

@author: anonym
"""

# Python3 program to compute Binomial 
# Probability 

# function to calculate nCr i.e., number of ways to choose r out of n objects (combinations)
def nCr(n, r): 
	
	# Since nCr is same as nC(n-r) 
	# To decrease number of iterations 
	if (r > n / 2): 
		r = n - r; 

	answer = 1; 
	for i in range(1, r + 1): 
		answer *= (n - r + i); 
		answer /= i; 

	return answer; 

# function to calculate binomial r.v. 
# probability 
def binomialProbability(n, k, p): 
	return (nCr(n, k) * pow(p, k) *
						pow(1 - p, n - k)); 

if __name__ == "__main__":
    
    import random
    # Driver code 
    n = 10; 
    
    p = 1.0 / 3; 
    summa=0
    P=[]
    for k in range(0,n+1,1):
        probability = binomialProbability(n, k, p); 
        summa+=probability
        P.append(probability)
        print("Probability of having", k, "heads when a coin is tossed", end = " "); 
        print(n, "times where probability of each head is", round(p, 6)); 
        print("is = ", round(probability, 6)); 
        
        # This code is contributed by mits 
        
    print("SOME ROUNDING:",round(summa,6))
    
    
    prob=[]
    
    for k in range(len(P)):
        prob.append(sum([P[i] for i in range(k+1)]))
    print(prob)
    for i in range(10):
            r = random.random()
            for p in prob:
                if r<p:
                    print("TRIAL:",i,"#HEADS:",prob.index(p))
                    break; #eventually number of heads is roughly the one imposed by the probability

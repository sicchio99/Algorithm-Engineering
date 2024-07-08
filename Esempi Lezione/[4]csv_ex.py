#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:31:51 2020

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

import csv
import time
import pandas as pd 
import os

rng.current = int(round(time.time() * 1000))
l=10

header = ["head"+str(i) for i in range(l)];
data1 = [round(rng(m)/m,2) for i in range(l)];
data2 = [round(rng(m)/m,2) for i in range(l)];
data3 = [round(rng(m)/m,2) for i in range(l)];

data=[header,data1,data2,data3]
filename='testfile.csv'
# os.remove(filename)
f = open(filename, 'w')

with f:

    writer = csv.writer(f)
    
    for row in data:
        writer.writerow(row)
        
        

f = open(filename, 'r')

with f:

    reader = csv.reader(f)

    for row in reader:
        print(row);
        

data = pd.read_csv(filename) 
print(data)
print(data[data.head0 > data.head3])
            
            
# # #COMPLEX OBJECTS
filename2='names.csv'
# os.remove(filename2)
f = open(filename2, 'w')

with f:
    
    fnames = ['first_name', 'last_name']
    writer = csv.DictWriter(f, fieldnames=fnames)    
    writer.writeheader()
    writer.writerow({'first_name' : 'John', 'last_name': 'Smith'})
    writer.writerow({'first_name' : 'Robert', 'last_name': 'Brown'})
    writer.writerow({'first_name' : 'Julia', 'last_name': 'Griffin'})
    
data = pd.read_csv(filename2) 
print(data)

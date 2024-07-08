# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 16:13:36 2023

@author: anonym
"""
#CODE TUNING

import time

cpu=time.perf_counter_ns()
res=0
counter=0
longer_array=list(range(1000000))
shorter_array=list(range(10))

for i in longer_array:
    counter+=1;
    for j in shorter_array:
        counter+=1;
        res+=i*j;
        
v1 = round(time.perf_counter_ns()-cpu,2)
print("loop v1:",counter,"time:",v1,"speedup",round(v1/v1,2))
print(res)

cpu=time.perf_counter_ns()
res=0
counter=0
for i in shorter_array:
    counter+=1;
    for j in longer_array:
        counter+=1;
        res+=i*j;
v2 = round(time.perf_counter_ns()-cpu,2)
print("loop v2:",counter,"time:",v2,"speedup",round(v1/v2,2))
print(res)

cpu=time.perf_counter_ns()
res=0
counter=0


for i in longer_array:
    counter+=1;    
    for j in range(4,len(shorter_array),4):
        
        counter+=4;
        res+=i*(j-3);
        res+=i*(j-2);
        res+=i*(j-1);
        res+=i*j;
        #OPTIONAL PARALLELISM
        
v3 = round(time.perf_counter_ns()-cpu,2)
print("loop v32:",counter,"time:",v3,"speedup",round(v1/v3,2))
print(res)
import matplotlib.pyplot as plt
data = {'v1': round(v1/v1,2), 'v2': round(v1/v2,2), 'v3': round(v1/v3,2)}
names = list(data.keys())
values = list(data.values())

fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True,dpi=600)
axs[0].bar(names, values)
axs[1].scatter(names, values)
axs[2].plot(names, values)
fig.suptitle('Speedups')

plt.show()
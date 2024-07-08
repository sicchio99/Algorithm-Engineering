#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:32:04 2020

@author: anonym
"""
from random import randrange

import time
from timeit import default_timer as timer


qcount=0;
bcount=0;
rcount=0;
# This function generates random pivot, swaps the first 
# element with the pivot and calls the partition fucntion. 
def partitionrand(arr , start, stop): 
  
    # Generating a random number between the  
    # starting index of the array and the 
    # ending index of the array. 
    randpivot = randrange(start, stop) 
  
    # Swapping the starting element of the array and the pivot 
    arr[start], arr[randpivot] = arr[randpivot], arr[start] 
    return partition(arr, start, stop) 

def randomizedquicksort(arr, start , stop): 
    if(start < stop): 
          
        # pivotindex is the index where  
        # the pivot lies in the array 
        pivotindex = partitionrand(arr, start, stop) 
          
        # At this stage the array is partially sorted  
        # around the pivot. Separately sorting the  
        # left half of the array and the right half of the array. 
        randomizedquicksort(arr , start , pivotindex - 1) 
        randomizedquicksort(arr, pivotindex + 1, stop) 
        
def partition(arr,low,high): 
    global qcount
    i = ( low-1 )         # index of smaller element 
    pivot = arr[high]     # pivot 
  
    for j in range(low , high): 
  
        # If current element is smaller than or 
        # equal to pivot 
        qcount+=1;
        if  arr[j] <= pivot: 
            # increment index of smaller element 
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i] 
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return ( i+1 ) 

# This function takes last element as pivot, places 
# the pivot element at its correct position in sorted 
# array, and places all smaller (smaller than pivot) 
# to left of pivot and all greater elements to right 
# of pivot 
def partition(arr,low,high): 
    global qcount
    i = ( low-1 )         # index of smaller element 
    pivot = arr[high]     # pivot 
  
    for j in range(low , high): 
  
        # If current element is smaller than or 
        # equal to pivot 
        qcount+=1;
        if  arr[j] <= pivot: 
            # increment index of smaller element 
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i] 
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return ( i+1 ) 
  
# The main function that implements QuickSort 
# arr[] --> Array to be sorted, 
# low  --> Starting index, 
# high  --> Ending index 
  
# Function to do Quick sort 
def quickSort(arr,low,high): 
    if low < high: 
  
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition(arr,low,high) 
  
        # Separately sort elements before 
        # partition and after partition 
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high) 
  
    
   
def test_equal(arr1,arr2):

 uguali=True;
 for c in range(len(arr2)):
     if arr1[c] != arr2[c]:
         uguali=False;
         break;
 return uguali;       

def test_larger(arr1,arr2):

 s1=[];
 s2=[];
 for c in range(len(arr2)):
     s1+=arr1[c];
     s2+=arr2[c];
 return s1>s2;   

def get_indices(statespace,terms):
    global rcount;
    indices=[]
    result = custom_binarySearch(statespace, 0, len(statespace)-1, terms) 
    orig=result;
    rcount+=1;
    while test_equal(statespace[(result-1)%len(statespace)],terms):
        indices.append(result-1)
        result-=1;
        rcount+=1;
    result=orig    
    # print(result)
    indices.append(result)
    rcount+=1;
    while test_equal(statespace[(result+1)%len(statespace)],terms):
        # print(result+1)
        indices.append(result+1)
        result+=1;    
        rcount+=1;
    return indices;          

# Returns index of x in arr if present, else -1 
def custom_binarySearch(arr, l, r, comparray): 
    global bcount
    # Check base case 
    if r >= l: 
  
        mid = l + (r - l)//2
        # If element is present at the middle itself 
        bcount+=1;
        if(test_equal(arr[mid],comparray)):    
            return mid
          
        # If element is smaller than mid, then it can only 
        # be present in left subarray 
        bcount+=1;
        if test_larger(arr[mid],comparray): 
            return custom_binarySearch(arr, l, mid-1, comparray) 
  
        # Else the element can only be present in right subarray 
        else: 
            return custom_binarySearch(arr, mid+1, r, comparray) 
  
    else: 
        # Element is not present in the array 
        return -1
    
# Driver code to test above 
# arr = ["cc","ca","b"]
# n = len(arr) 
# quickSort(arr,0,n-1) 
# print ("Sorted array is:") 
# for i in range(n): 
#     print (arr[i]) 
    
    
# Text="""bands which have connected them with another, and to assume among the powers of the earth, 
# the separate and equal station to which the Laws of Nature and of Nature's God entitle them, 
# a decent respect to the opinions of mankind requires that they should declare 
# the causes which impel them to the separation.  We hold these truths to be
# self-evident, that all men are created equal, that they are endowed by their 
# Creator with certain unalienable Rights, that among these are Life, Liberty 
# and the pursuit of Happiness.--That to secure these rights, Governments are 
# instituted among Men, deriving their just powers from the consent of the governed
# , --That whenever any Form of Government becomes destructive of these ends, it 
# is the Right of the People to alter or to abolish it, and to institute new 
# Government, laying its foundation on such principles and organizing its
# powers in such form, as to them shall seem most likely to effect their 
# Safety and Happiness. """

if __name__ == "__main__":
    
    Text="this is a test this is only a test this is a test of the emergency broadcasting system. That "\
        "whenever any Form of Government becomes destructive of these ends, it is the Right of the People to alter or to abolish it"
    
    # Cleaning text and lower casing all words
    for char in '-.,\n':
        Text=Text.replace(char,' ')
    
    Text = Text.lower()
    
    # print(Text)
    
    words=Text.split()
    
    # 	
    k=1
    wordsleft=50

    
    #Building dictionary
    statespace=[]
    counter = 0;
    for word in words:
        triple=[]
        triple.append(word)
        triple.append(words[(counter+1)%len(words)])
        triple.append(words[(counter+2)%len(words)])
        triple.append((counter+2)%len(words))
        counter+=1;
        statespace.append(triple)

    # import math    
    # print(len(statespace)*math.log10(len(statespace)))
    
    # quickSort(statespace,0,len(statespace)-1) 
    print("SORTING")

    randomizedquicksort(statespace,0,len(statespace)-1) 
    print("STATE SPACE")
    for i in statespace:
        print(i)    
    phrase = [];
    
    nword=len(words)
    
    print("INITIALIZATION")

    # print(nword)
    output=[]
    for i in range(k):
        phrase.append(words[i])
        output.append(words[i])
    print("P: "+str(phrase))

    wordsleft=wordsleft-k

    wall=time.time();
    perf_count=time.perf_counter();
    cpu=timer();
    t = time.process_time()
    
    print("GENERATION")

    for i in range(wordsleft,0,-1):
    
            #indices of phrase        
            """BINARY SEARCH"""
            idx = get_indices(statespace,phrase)
            #random lookup
            # print (idx)
            # print (idx[0])
            # print ()
            # next = randrange(len(idx))
            # print(next)
            # print(statespace[idx[randrange(len(idx))]][k])
            
            """RANDOM LOOKUP"""
            word_to_add = statespace[idx[randrange(len(idx))]][k];
            # print(word_to_add)
            output.append(word_to_add)
            # print(output)
            # print("P1: "+str(phrase))
            del phrase[0]
           
            phrase.append(word_to_add)
    
    for word in output: 	
        print(word+ " ", end = '')
      
    #exercise replicate experimentation with other texts
    print("\nQCOUNT:",qcount)
    print("BCOUNT:",bcount)
    print("RCOUNT:",rcount)
    
    #VARIOUS TIMERS
    print(round(time.process_time()-t,6),round(timer()-cpu,6),round(time.perf_counter()-perf_count,6),round(time.time()-wall,6))

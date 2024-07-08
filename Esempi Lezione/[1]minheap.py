# Python3 implementation of Min Heap 


from heapq import heappush, heappop
import math

def Left(i):
    return 2*i+1;

def Right(i):
    return 2*i+2;

def Parent(i):
    return math.floor(i/2);

def heapify(A,i,n,maxh=True):
    l = Left(i);
    r = Right(i);
    if maxh:
        if l < n and A[l] > A[i]:
            Largest = l
        else:
            Largest = i
        if r < n and A[r] > A[Largest]:
            Largest = r;
        if Largest != i:
            A[i], A[Largest]=A[Largest],A[i]
            heapify(A,Largest,n,maxh);   
    else:
        if l < n and A[l] < A[i]:
            Smallest = l
        else:
            Smallest = i
        if r < n and A[r] < A[Smallest]:
            Smallest = r;
       
        if Smallest != i:
            A[i],A[Smallest]=A[Smallest],A[i]
            heapify(A,Smallest,n,maxh);     

def build(A,maxh=True):
    for i in range(math.floor(len(A)/2),-1,-1): #for i=n/2 to 0
        # print(i)
        heapify(A,i,len(A),maxh)
        
def is_heap_assert(A,maxh=True):
    for index in range(len(A)):
        if maxh:
            if Left(index)<len(A):
                assert A[index]>=A[Left(index)]
            if Right(index)<len(A):
                assert A[index]>=A[Right(index)]
            assert A[index]<=A[Parent(index)]
        else:
            if Left(index)<len(A):
                assert A[index]<=A[Left(index)]
            if Right(index)<len(A):
                assert A[index]<=A[Right(index)]
            assert A[index]>=A[Parent(index)] 
        
        # print(index,A[index],A[Left(index)],A[Right(index)])
        
def is_heap(A,maxh=True):
    for index in range(len(A)):
        if maxh:
            if Left(index)<len(A):
                if not A[index]>=A[Left(index)]:
                    return False
            if Right(index)<len(A):
                if not A[index]>=A[Right(index)]:
                    # return False
                    raise Exception('not a heap')

            if not A[index]<=A[Parent(index)]:
                return False
        else:
            if not (A[index]<=A[Left(index)] and A[index]<=A[Right(index)] and A[index]>=A[Parent(index)]):
                return False
            # assert A[index]<=A[Left(index)]
            # assert A[index]<=A[Right(index)]
            # assert A[index]>=A[Parent(index)] 
        
        # print(index,A[index],A[Left(index)],A[Right(index)])
    return True
#TESTS FOR CORRECTNESS AGAINST BUILTIN HEAP

heap = []
data = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]

homemadeheap=data.copy();
print("INPUT",homemadeheap)

build(homemadeheap,True)
print("HOMEMADE MAX HEAP INPUT",homemadeheap)
print(homemadeheap[6])
old_v = homemadeheap[6]
homemadeheap[6]=11
# print("HOMEMADE MAX HEAP INPUT",homemadeheap)
# homemadeheap[6]=old_v
# assert is_heap(homemadeheap,True)
is_heap_assert(homemadeheap,True)

build(homemadeheap,False)
print("HOMEMADE MIN HEAP INPUT (INPUT MAX)",homemadeheap)

homemadeheap=data.copy();
build(homemadeheap,False)
print("HOMEMADE MIN HEAP INPUT (INPUT ORIGINAL)",homemadeheap)

for item in data:
    heappush(heap, item)
    
ordered = []
aux = data.copy();

print("PYTHON HEAP INPUT",heap)

#HEAPSORT
while heap:
   element = heappop(heap);
   assert element == min(aux)
   #increases running time of test program (remove during workhorse)
   print("MIN HEAP ELEMENT:",element)
   print("MIN SEARCH ELEMENT:",min(aux))
   aux.remove(element)
   print("REMAINING VECTOR",aux)
   ordered.append(element);
   
print("SORTED",ordered)




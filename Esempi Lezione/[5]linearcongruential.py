
from math import gcd as bltin_gcd

def coprime2(a, b):
    return bltin_gcd(a, b) == 1;

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if (n % i)!=0:
            i += 1
        else:
            n //= i
            if i not in factors:
                factors.append(i)
          
    if n > 1:
        if n not in factors:
            factors.append(n)
    return factors


m = 2**32;
b = 12345;
a = 1103515245;

# a-1 multiple of 4 since m multiple of 4
# a-1 is divisible by all prime factors of m
# b and m relatively prime

print(coprime2(m,b))
print((a-1)%4==0)
fact=prime_factors(m)

for f in fact: 
    print((a-1)%f==0)

def rng(M=m, A=a, B=b):
    rng.current = (A*rng.current + B) % M
    return rng.current


import time

# setting the seed
# rng.current = 1
rng.current = int(round(time.time() * 1000))

#vector of random integers
vector = [rng(m) for i in range(10)];

print(vector)

#vector of random floats
vector = [rng(m)/m for i in range(10)];
print(vector)

#vector of random integers within range start,end
start=5
end=25
vector = [start + round((rng(m)/m)*(end-start+1)) for i in range(10)];
print(vector)
#vector of random floats within range start,end
start=5
end=25
vector = [start + (rng(m)/m)*(end-start) for i in range(10)];
print(vector)

#EXERCISE - DEVELOP IN C++
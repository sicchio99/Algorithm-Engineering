import numpy
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

x = [1,2,3,5,6,7,8,9,10,12,13,14,15,16,18,19,21,22]
y = [100,90,80,60,60,55,60,65,70,70,75,76,78,79,90,99,99,100]

mymodel = numpy.poly1d(numpy.polyfit(x, y, 3))
print(mymodel)
myline = numpy.linspace(1, 22, 100)#solo per ascissa del plot




print(r2_score(y, mymodel(x))) 
"""
The result 0.94 shows that there is a very good relationship, 
and we can use polynomial regression in future predictions.
"""


x = [89,43,36,36,95,10,66,34,38,20,26,29,48,64,6,5,36,66,72,40]
y = [21,46,3,35,67,95,53,72,58,10,26,34,90,33,38,20,56,2,47,15]

mymodel = numpy.poly1d(numpy.polyfit(x, y, 3))
print(mymodel)
print(r2_score(y, mymodel(x)))
"""


The result: 0.00995 indicates a very bad relationship, and 
tells us that this data set is not suitable for polynomial regression.

"""

import random
x = [i for i in range(1,100)]
y = [i*i*i + 2*i*i + random.random()**2%(i**2) for i in x] #adding some noise
mymodel = numpy.poly1d(numpy.polyfit(x, y, 3))
print(mymodel)
print("QUERY MODEL FOR PREDICTIONS")
print("PREDICTION for 25 (should be 25^3+2*25^2=16875): ",mymodel(25))
print(r2_score(y, mymodel(x))) 
"""1.0 means PERFECT FIT"""

plt.scatter(x, y)
plt.plot(myline, mymodel(myline))
plt.show() 



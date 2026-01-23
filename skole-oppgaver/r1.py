import math
import matplotlib.pyplot as plt
import numpy as np
h = 0.001
a=--4
b=3
area = 0


x=-4
def f(x):
    return math.log((x**2)+(3*x) +6)
def g(x):
    return (f(x+h)-f(x))/(h)

xverdier=[]
yverdier=[]
x_1=[]
y_1=[]

while x<=3:
    xverdier.append(x)
    yverdier.append(g(x))
    x_1.append(x)
    y_1.append(f(x))
   
    x=x+0.1

    
print (area)

plt.xlabel('x')
plt.ylabel('funksjoner')
plt.grid(True)
plt.plot(x_1, y_1)
plt.plot(xverdier, yverdier)    
plt.show()


    

    


    
    
    

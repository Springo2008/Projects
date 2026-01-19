import math
import matplotlib.pyplot as plt
import numpy as np
h = 0.00000001
x=-10
def f(x):
    return math.log((x**2) +1)
def g(x):
    return (f(x+h)-f(x))/(h)

xverdier=[]
yverdier=[]
x_1=[]
y_1=[]

while x<=10:
    xverdier.append(x)
    yverdier.append(g(x))
    x_1.append(x)
    y_1.append(f(x))
    x=x+0.001
plt.plot(x_1, y_1)    
plt.plot(xverdier, yverdier)
plt.show()

    


    
    
    

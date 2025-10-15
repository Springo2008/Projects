import numpy as np

x = 0.0001

def a():
    return (1+x)**(1/x)

while x > 0.0000000001:
    print(a())
    x = x / 10
    print(x)
    print(a()-np.e)
    
    
print("lim(x->0) (1+x)^(1/x) = e ≠", a())

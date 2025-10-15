import numpy as np
x = 0.0001
def a(x):
    return (((np.e)**(x+1))-(np.e))/x
while x > 0.0000000001:
    print(a(x))
    x = x / 10
    print(x)
    print(a(x)-np.e)
print("lim(x->0) (e^(x+1)-e)/x = e =", a(x))
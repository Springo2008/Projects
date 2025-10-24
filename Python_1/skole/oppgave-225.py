import numpy as np
def f(x):
    return ((2*x**2)-x+11)/((x**3)-8)

# lim x-> inf f(x)
x_values = np.linspace(100, 1000, num=10)
f_values = f(x_values)
limit_inf = f_values[-1]
print(f"Lim x-> inf f(x) = {limit_inf}")


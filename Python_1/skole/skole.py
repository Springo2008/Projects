def f(x):
    return x**2 +x + 1

start=3
slutt=2

while start<=slutt:
    x_verdi=start
    y_verdi=f(start)
    print (x_verdi, y_verdi)
    start -= 0.1

    print (f(start))
    
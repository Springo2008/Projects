import math

input = float(input("Velg et tall: "))

kvadratroten = math.sqrt(input)
er_kvadrattall = kvadratroten * kvadratroten == input

kubikkrot = round(input ** (1/3))
er_kubikktall = kubikkrot * kubikkrot * kubikkrot == input

if er_kvadrattall:
    print("tallet er et kvadrattall")
elif er_kubikktall:
    print("tallet er et kubikktall")
else:
    print("tallet er verken et kvadrattall eller et kubikktall")


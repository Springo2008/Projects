antall = int(input("Hvor mange figurer vil du lage? "))

def figur(n):
    klosser = 0
    for i in range(1, n+1):
        klosser += i**2
    return klosser

print(f"Du trenger {figur(antall)} klosser for å lage {antall} figurer.")

# Hvor mange figurer kan du lage med 10 000 klosser?
beholding = 10000
n = 1

while beholding >= n**2:
    beholding -= n**2
    n += 1

print(f"Med 10000 klosser kan du lage {n-1} figurer og har {beholding} klosser igjen.")

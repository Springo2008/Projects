s = 0  # Startposisjon i meter
v = 0  # Startfart i m/s
t = 0  # Starttid i sekunder
s_slutt = 0.40  # Sluttposisjon i meter
dt = 0.000001  # Tidssteg for simuleringen

def a(s):
    aks = (300 / (s + 0.01))  # Beregner akselerasjonen basert på posisjon s
    return aks  # Returnerer akselerasjonen

# Løkke som kjører så lenge posisjonen s er mindre enn sluttposisjonen s_slutt
while s < s_slutt:
    v = v + a(s) * dt  # Oppdaterer fart v basert på akselerasjonen
    s = s + v * dt  # Oppdaterer posisjon s basert på den nye farten
    t = t + dt  # Oppdaterer tid t med tidssteget dt

# Skriver ut den endelige farten, justert for tidssteget
print("fart", v - v * dt, "m/s")
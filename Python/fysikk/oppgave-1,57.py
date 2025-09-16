v_0 = 8.0  # m/s
a = -9.81  # m/s^2
t_total = 2  # sekunder
dt = 0.01  # tidssteg i sekunder

s = 0
v = v_0
t = 0

while t < t_total:
    s += v * dt
    v += a * dt
    t += dt

print(s)
# Numerisk svar, bør være nær -3.6 m

#oppgave b) Finn posisjonen ved hjelp av bevegelses likningen for konstant akselerasjon og sammenling med oppgave a
s_1 = v_0 * t_total + 0.5 * a * t_total**2
print(s_1)
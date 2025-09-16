# Bevegelseslikninger og simuleringer - Casio fx-CG50 Python

v_0 = 8.0      # starthastighet (m/s)
a = -9.81      # akselerasjon (m/s^2)
t_total = 2.0  # total tid (s)
dt = 0.01      # tidssteg (s)

# 1. Simulering: s = v_0 * t + 0.5 * a * t**2
s1 = 0
t = 0
while t < t_total:
    s1 = v_0 * t + 0.5 * a * t**2
    t += dt
print("Simulert posisjon (s = v_0*t + 0.5*a*t^2):", s1)

# 2. Simulering: v = v_0 + a * t
v2 = v_0
t = 0
while t < t_total:
    v2 = v_0 + a * t
    t += dt
print("Simulert fart (v = v_0 + a*t):", v2)

# 3. Simulering: s = (v**2 - v_0**2) / (2 * a)
v3 = v_0
t = 0
while t < t_total:
    v3 = v_0 + a * t
    s3 = (v3**2 - v_0**2) / (2 * a)
    t += dt
print("Simulert posisjon (s = (v^2 - v_0^2)/(2*a)):", s3)

# 4. Simulering: s = ((v_0 + v) / 2) * t
v4 = v_0
t = 0
while t < t_total:
    v4 = v_0 + a * t
    s4 = ((v_0 + v4) / 2) * t
    t += dt
print("Simulert posisjon (s = ((v_0 + v)/2)*t):", s4)

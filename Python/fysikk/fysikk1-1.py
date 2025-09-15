import numpy as np
import matplotlib.pyplot as plt

# startverdier
y0 = 1.0       
v0 = 15.0     
g = 9.81       


a = 0.5 * g
b = -v0
c = -y0


disk = b**2 - 4*a*c
t1 = (-b + np.sqrt(disk)) / (2*a)
t2 = (-b - np.sqrt(disk)) / (2*a)


t_slutt = max(t1, t2)

print(f"Ballen treffer bakken etter ca {t_slutt:.2f} sekunder")


t = np.linspace(0, t_slutt, 200)
y = y0 + v0*t - 0.5*g*t**2

f
plt.plot(t, y, label="Ballens bane")
plt.axhline(0, color="gray", linestyle="--")  # bakken
plt.xlabel("Tid (s)")
plt.ylabel("Høyde (m)")
plt.title("Ball kastet opp med 15 m/s fra 1 m høyde")
plt.legend()
plt.grid(True)
plt.show()

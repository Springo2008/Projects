import math
v_0=120/3.6  # initial speed in m/s
v_1=0 # final speed in m/s
m=800 # mass in kg
mu=0.7 # frictioncoefficient kg/m on wheels on road
g=9.81 # gravity m/s^2
k=0.47 # kg/m air resistance coefficient

f=mu*m*g # friction force in N
a=-f/m
s=(v_1**2-v_0**2)/(2*a) # braking distance in meters
print(f"Initialhastighet: {v_0:.2f} m/s ({v_0*3.6:.0f} km/h)")
print(f"Friksjonkraft: {f:.2f} N")
print(f"Akselerasjon: {a:.2f} m/s²")
print(f"Bremselengde: {s:.2f} meter")



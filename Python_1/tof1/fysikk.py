from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
v= 0
v_liste=[v]
data = pd.read_csv('/Users/husby/Downloads/Raw Data.csv')
time = data["Time (s)"]
accelerationx = data["Linear Acceleration x (m/s^2)"]
accelerationy = data["Linear Acceleration y (m/s^2)"]
accelerationz = data["Linear Acceleration z (m/s^2)"]

plt.plot(time, accelerationx, label='Akselerasjon x (m/s^2)')
plt.plot(time, accelerationy, label='Akselerasjon y (m/s^2)')
plt.plot(time, accelerationz, label='Akselerasjon z (m/s^2)')
plt.legend()
plt.show()

print("accelerationy:", data["Linear Acceleration y (m/s^2)"].mean())

for i in range(len(time)-1):
    delta_v=(time[i+1]-time[i])*accelerationy[i]
    v=v+delta_v
    v_liste.append(v)
    
plt.title("Hastighet y (m/s)")
plt.plot(time, v_liste, label='Hastighet y (m/s)')
plt.xlabel("Tid (s)")
plt.ylabel("Hastighet (m/s)")
plt.legend()
plt.show()

print("Maks hastighet y (m/s):", round(max((v_liste)), 2), "m/s")
    
    
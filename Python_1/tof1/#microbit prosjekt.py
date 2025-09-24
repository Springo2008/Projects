#microbit prosjekt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # Legg til denne importen

# Initialiser variabler for alle akser
vx, vy, vz = 0, 0, 0
sx, sy, sz = 0, 0, 0
vx_liste = [vx]
vy_liste = [vy]
vz_liste = [vz]
sx_liste = [sx]
sy_liste = [sy]
sz_liste = [sz]

# Les data fra CSV-fil
data = pd.read_csv('/Users/husby/Downloads/Acceleration without g 2025-01-15 13-16-22/Raw Data.csv')
#data = pd.read_csv("/Users/husby/Downloads/Raw Data.csv")

time = data["Time (s)"]
accelerationx = data["Linear Acceleration x (m/s^2)"]
accelerationy = data["Linear Acceleration y (m/s^2)"]
accelerationz = data["Linear Acceleration z (m/s^2)"]

# Beregn total akselerasjon (magnitude)
total_acceleration = np.sqrt(accelerationx**2 + accelerationy**2 + accelerationz**2)

# Fjern offset (gjennomsnitt) fra alle akser
acceleration_x_adj = accelerationx - accelerationx.mean()
acceleration_y_adj = accelerationy - accelerationy.mean()
acceleration_z_adj = accelerationz - accelerationz.mean()

# Beregn hastighet og posisjon for alle akser
for i in range(len(time)-1):
    dt = time.iloc[i+1] - time.iloc[i]  # Tidsintervall
    
    # X-akse
    delta_vx = dt * acceleration_x_adj.iloc[i]
    vx = vx + delta_vx
    vx_liste.append(vx)
    delta_sx = dt * vx
    sx = sx + delta_sx
    sx_liste.append(sx)
    
    # Y-akse
    delta_vy = dt * acceleration_y_adj.iloc[i]
    vy = vy + delta_vy
    vy_liste.append(vy)
    delta_sy = dt * vy
    sy = sy + delta_sy
    sy_liste.append(sy)
    
    # Z-akse
    delta_vz = dt * acceleration_z_adj.iloc[i]
    vz = vz + delta_vz
    vz_liste.append(vz)
    delta_sz = dt * vz
    sz = sz + delta_sz
    sz_liste.append(sz)

# Beregn total hastighet og posisjon
total_hastighet = [np.sqrt(vx_liste[i]**2 + vy_liste[i]**2 + vz_liste[i]**2) for i in range(len(vx_liste))]
total_posisjon = [np.sqrt(sx_liste[i]**2 + sy_liste[i]**2 + sz_liste[i]**2) for i in range(len(sx_liste))]

# Plot alle akser
plt.figure(figsize=(18, 12))

# Plot akselerasjon
plt.subplot(3, 4, 1)
plt.plot(time, accelerationx, label="x", color='red')
plt.plot(time, accelerationy, label="y", color='green')
plt.plot(time, accelerationz, label="z", color='blue')
plt.plot(time, total_acceleration, label="total", color='black', linestyle='--')
plt.title("Akselerasjon")
plt.xlabel("Tid (s)")
plt.ylabel("Akselerasjon (m/s²)")
plt.legend()
plt.grid(True)

# Plot hastighet - alle akser
plt.subplot(3, 4, 2)
plt.plot(time, vx_liste, label="vx", color='red')
plt.plot(time, vy_liste, label="vy", color='green')
plt.plot(time, vz_liste, label="vz", color='blue')
plt.plot(time, total_hastighet, label="total", color='black', linestyle='--')
plt.title("Hastighet - Alle akser")
plt.xlabel("Tid (s)")
plt.ylabel("Hastighet (m/s)")
plt.legend()
plt.grid(True)

# Plot posisjon - alle akser
plt.subplot(3, 4, 3)
plt.plot(time, sx_liste, label="sx", color='red')
plt.plot(time, sy_liste, label="sy", color='green')
plt.plot(time, sz_liste, label="sz", color='blue')
plt.plot(time, total_posisjon, label="total", color='black', linestyle='--')
plt.title("Posisjon - Alle akser")
plt.xlabel("Tid (s)")
plt.ylabel("Posisjon (m)")
plt.legend()
plt.grid(True)

# Plot hastighet X-akse
plt.subplot(3, 4, 4)
plt.plot(time, vx_liste, color='red')
plt.title("Hastighet X-akse")
plt.xlabel("Tid (s)")
plt.ylabel("Hastighet (m/s)")
plt.grid(True)

# Plot hastighet Y-akse
plt.subplot(3, 4, 5)
plt.plot(time, vy_liste, color='green')
plt.title("Hastighet Y-akse")
plt.xlabel("Tid (s)")
plt.ylabel("Hastighet (m/s)")
plt.grid(True)

# Plot hastighet Z-akse
plt.subplot(3, 4, 6)
plt.plot(time, vz_liste, color='blue')
plt.title("Hastighet Z-akse")
plt.xlabel("Tid (s)")
plt.ylabel("Hastighet (m/s)")
plt.grid(True)

# Plot posisjon X-akse
plt.subplot(3, 4, 7)
plt.plot(time, sx_liste, color='red')
plt.title("Posisjon X-akse")
plt.xlabel("Tid (s)")
plt.ylabel("Posisjon (m)")
plt.grid(True)

# Plot posisjon Y-akse
plt.subplot(3, 4, 8)
plt.plot(time, sy_liste, color='green')
plt.title("Posisjon Y-akse")
plt.xlabel("Tid (s)")
plt.ylabel("Posisjon (m)")
plt.grid(True)

# Plot posisjon Z-akse
plt.subplot(3, 4, 9)
plt.plot(time, sz_liste, color='blue')
plt.title("Posisjon Z-akse")
plt.xlabel("Tid (s)")
plt.ylabel("Posisjon (m)")
plt.grid(True)

# Beregn resultater for alle akser
total_tid = time.iloc[-1] - time.iloc[0]

# X-akse resultater
maks_hastighet_x = max(vx_liste)
min_hastighet_x = min(vx_liste)
total_avstand_x = abs(sx_liste[-1] - sx_liste[0])
gjennomsnitt_hastighet_x = total_avstand_x / total_tid if total_tid > 0 else 0

# Y-akse resultater  
maks_hastighet_y = max(vy_liste)
min_hastighet_y = min(vy_liste)
total_avstand_y = abs(sy_liste[-1] - sy_liste[0])
gjennomsnitt_hastighet_y = total_avstand_y / total_tid if total_tid > 0 else 0

# Z-akse resultater
maks_hastighet_z = max(vz_liste)
min_hastighet_z = min(vz_liste)
total_avstand_z = abs(sz_liste[-1] - sz_liste[0])
gjennomsnitt_hastighet_z = total_avstand_z / total_tid if total_tid > 0 else 0

# Total resultater
maks_hastighet_total = max(total_hastighet)
total_avstand_total = np.sqrt(total_avstand_x**2 + total_avstand_y**2 + total_avstand_z**2)
gjennomsnitt_hastighet_total = total_avstand_total / total_tid if total_tid > 0 else 0

print("=== AKSELERASJON ANALYSE ===")
print(f"Gjennomsnitt x-akselerasjon: {round(accelerationx.mean(), 3)} m/s²")
print(f"Gjennomsnitt y-akselerasjon: {round(accelerationy.mean(), 3)} m/s²")
print(f"Gjennomsnitt z-akselerasjon: {round(accelerationz.mean(), 3)} m/s²")
print(f"Maks total akselerasjon: {round(total_acceleration.max(), 3)} m/s²")

print("\n=== HASTIGHET RESULTATER ===")
print(f"X-akse - Maks: {round(maks_hastighet_x, 2)} m/s, Min: {round(min_hastighet_x, 2)} m/s, Gj.snitt: {round(gjennomsnitt_hastighet_x, 2)} m/s")
print(f"Y-akse - Maks: {round(maks_hastighet_y, 2)} m/s, Min: {round(min_hastighet_y, 2)} m/s, Gj.snitt: {round(gjennomsnitt_hastighet_y, 2)} m/s")
print(f"Z-akse - Maks: {round(maks_hastighet_z, 2)} m/s, Min: {round(min_hastighet_z, 2)} m/s, Gj.snitt: {round(gjennomsnitt_hastighet_z, 2)} m/s")
print(f"Total - Maks: {round(maks_hastighet_total, 2)} m/s, Gj.snitt: {round(gjennomsnitt_hastighet_total, 2)} m/s")

print("\n=== AVSTAND/LENGDE RESULTATER ===")
print(f"X-akse avstand: {round(total_avstand_x, 2)} m")
print(f"Y-akse avstand: {round(total_avstand_y, 2)} m") 
print(f"Z-akse avstand: {round(total_avstand_z, 2)} m")
print(f"Total 3D avstand: {round(total_avstand_total, 2)} m")
print(f"Total tid: {round(total_tid, 2)} s")

# Tekstboks med sammendrag
results_text = f"""Sammendrag alle akser:
• Maks hastighet total: {round(maks_hastighet_total, 2)} m/s
• Gj.snitt hastighet total: {round(gjennomsnitt_hastighet_total, 2)} m/s
• Total 3D avstand: {round(total_avstand_total, 2)} m
• X-avstand: {round(total_avstand_x, 2)} m
• Y-avstand: {round(total_avstand_y, 2)} m  
• Z-avstand: {round(total_avstand_z, 2)} m
• Total tid: {round(total_tid, 2)} s"""

plt.subplot(3, 4, 10)
plt.text(0.05, 0.5, results_text, fontsize=9, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"),
         verticalalignment='center')
plt.axis('off')
plt.title("Sammendrag")

# 3D bane plot - FIKSET VERSJON
plt.subplot(3, 4, 11)
ax = plt.axes(projection='3d')  # Endret fra gca(projection='3d')
ax.plot3D(sx_liste, sy_liste, sz_liste, color='purple')  # Bruk plot3D
ax.set_xlabel('X posisjon (m)')
ax.set_ylabel('Y posisjon (m)')
ax.set_zlabel('Z posisjon (m)')
ax.set_title('3D Bevegelse')

plt.tight_layout()
plt.show()

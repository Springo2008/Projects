#microbit prosjekt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # Legg til denne importen

# Les data fra CSV-fil
data = pd.read_csv('/Users/husby/Downloads/Acceleration without g 2025-01-15 13-16-22/Raw Data.csv')
#data = pd.read_csv("/Users/husby/Downloads/Raw Data.csv")

# FJERN DE FØRSTE 10 SEKUNDENE
data = data[data["Time (s)"] >= 10.0].reset_index(drop=True)

# Nullstill tiden så den starter på 0
data["Time (s)"] = data["Time (s)"] - data["Time (s)"].iloc[0]

time = data["Time (s)"]
accelerationx = data["Linear Acceleration x (m/s^2)"]
# BYTT Y OG Z SIDEN Z ER FAKTISK VERTIKAL AKSE
accelerationy = data["Linear Acceleration z (m/s^2)"]  # Z-data brukes som Y (vertikal)
accelerationz = data["Linear Acceleration y (m/s^2)"]  # Y-data brukes som Z (horisontal)

# Initialiser variabler for alle akser
vx, vy, vz = 0, 0, 0
sx, sy, sz = 0, 0, 0
vx_liste = [vx]
vy_liste = [vy]
vz_liste = [vz]
sx_liste = [sx]
sy_liste = [sy]
sz_liste = [sz]

# Beregn total akselerasjon (magnitude)
total_acceleration = np.sqrt(accelerationx**2 + accelerationy**2 + accelerationz**2)

# Fjern offset (gjennomsnitt) fra alle akser
acceleration_x_adj = accelerationx - accelerationx.mean()
acceleration_y_adj = accelerationy - accelerationy.mean()
acceleration_z_adj = accelerationz - accelerationz.mean()

# Første integrasjon (hastighet)
for i in range(len(time)-1):
    dt = time.iloc[i+1] - time.iloc[i]  # Tidsintervall
    
    # X-akse
    delta_vx = dt * acceleration_x_adj.iloc[i]
    vx = vx + delta_vx
    vx_liste.append(vx)
    
    # Y-akse (vertikal - fra Z-data)
    delta_vy = dt * acceleration_y_adj.iloc[i]
    vy = vy + delta_vy
    vy_liste.append(vy)
    
    # Z-akse (horisontal - fra Y-data)
    delta_vz = dt * acceleration_z_adj.iloc[i]
    vz = vz + delta_vz
    vz_liste.append(vz)

# KORREKSJON FOR HEIS: Fjern lineær drift fra hastighet for x og z (skal ende på 0)
total_time = time.iloc[-1] - time.iloc[0]

# Beregn og fjern lineær drift for x-hastighet
vx_drift = vx_liste[-1] / len(vx_liste)
vx_liste_corrected = [vx_liste[i] - vx_drift * i for i in range(len(vx_liste))]

# Beregn og fjern lineær drift for z-hastighet  
vz_drift = vz_liste[-1] / len(vz_liste)
vz_liste_corrected = [vz_liste[i] - vz_drift * i for i in range(len(vz_liste))]

# Y-hastighet beholdes som den er (heis beveger seg opp/ned)
vy_liste_corrected = vy_liste.copy()

# Andre integrasjon (posisjon) med korrigerte hastigheter
sx, sy, sz = 0, 0, 0
sx_liste = [sx]
sy_liste = [sy] 
sz_liste = [sz]

for i in range(len(time)-1):
    dt = time.iloc[i+1] - time.iloc[i]
    
    # X-akse (korrigert)
    delta_sx = dt * vx_liste_corrected[i]
    sx = sx + delta_sx
    sx_liste.append(sx)
    
    # Y-akse (vertikal)
    delta_sy = dt * vy_liste_corrected[i]
    sy = sy + delta_sy
    sy_liste.append(sy)
    
    # Z-akse (korrigert)
    delta_sz = dt * vz_liste_corrected[i]
    sz = sz + delta_sz
    sz_liste.append(sz)

# Bruk korrigerte verdier for plotting
vx_liste = vx_liste_corrected
vz_liste = vz_liste_corrected
vy_liste = vy_liste_corrected

# Beregn total hastighet og posisjon
total_hastighet = [np.sqrt(vx_liste[i]**2 + vy_liste[i]**2 + vz_liste[i]**2) for i in range(len(vx_liste))]
total_posisjon = [np.sqrt(sx_liste[i]**2 + sy_liste[i]**2 + sz_liste[i]**2) for i in range(len(sx_liste))]

# Plot - fokusert på Y-akse (vertikal)
plt.figure(figsize=(18, 10))

# Plot akselerasjon - alle akser
plt.subplot(2, 4, 1)
plt.plot(time, accelerationx, label="x", color='red')
plt.plot(time, accelerationy, label="y (vertikal)", color='green')
plt.plot(time, accelerationz, label="z", color='blue')
plt.plot(time, total_acceleration, label="total", color='black', linestyle='--')
plt.title("Akselerasjon")
plt.xlabel("Tid (s)")
plt.ylabel("Akselerasjon (m/s²)")
plt.legend()
plt.grid(True)

# Plot hastighet - alle akser
plt.subplot(2, 4, 2)
plt.plot(time, vx_liste, label="vx", color='red')
plt.plot(time, vy_liste, label="vy (vertikal)", color='green')
plt.plot(time, vz_liste, label="vz", color='blue')
plt.plot(time, total_hastighet, label="total", color='black', linestyle='--')
plt.title("Hastighet - Alle akser")
plt.xlabel("Tid (s)")
plt.ylabel("Hastighet (m/s)")
plt.legend()
plt.grid(True)

# Plot posisjon - alle akser
plt.subplot(2, 4, 3)
plt.plot(time, sx_liste, label="sx", color='red')
plt.plot(time, sy_liste, label="sy (vertikal)", color='green')
plt.plot(time, sz_liste, label="sz", color='blue')
plt.plot(time, total_posisjon, label="total", color='black', linestyle='--')
plt.title("Posisjon - Alle akser")
plt.xlabel("Tid (s)")
plt.ylabel("Posisjon (m)")
plt.legend()
plt.grid(True)

# Plot hastighet Y-akse (vertikal heis-bevegelse)
plt.subplot(2, 4, 4)
plt.plot(time, vy_liste, color='green')
plt.title("Hastighet Y-akse (vertikal)")
plt.xlabel("Tid (s)")
plt.ylabel("Hastighet (m/s)")
plt.grid(True)

# Plot posisjon Y-akse (vertikal heis-bevegelse)
plt.subplot(2, 4, 5)
plt.plot(time, sy_liste, color='green')
plt.title("Posisjon Y-akse (vertikal)")
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

# Y-akse resultater (vertikal)
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

print("=== HEIS ANALYSE ===")
print(f"Sluttposisjon X: {round(sx_liste[-1], 4)} m (skal være ~0)")
print(f"Sluttposisjon Y (vertikal): {round(sy_liste[-1], 4)} m") 
print(f"Sluttposisjon Z: {round(sz_liste[-1], 4)} m (skal være ~0)")

print("\n=== AKSELERASJON ANALYSE ===")
print(f"Gjennomsnitt x-akselerasjon: {round(accelerationx.mean(), 3)} m/s²")
print(f"Gjennomsnitt y-akselerasjon (vertikal): {round(accelerationy.mean(), 3)} m/s²")
print(f"Gjennomsnitt z-akselerasjon: {round(accelerationz.mean(), 3)} m/s²")
print(f"Maks total akselerasjon: {round(total_acceleration.max(), 3)} m/s²")

print("\n=== HASTIGHET RESULTATER ===")
print(f"X-akse - Maks: {round(maks_hastighet_x, 2)} m/s, Min: {round(min_hastighet_x, 2)} m/s, Gj.snitt: {round(gjennomsnitt_hastighet_x, 2)} m/s")
print(f"Y-akse (vertikal) - Maks: {round(maks_hastighet_y, 2)} m/s, Min: {round(min_hastighet_y, 2)} m/s, Gj.snitt: {round(gjennomsnitt_hastighet_y, 2)} m/s")
print(f"Z-akse - Maks: {round(maks_hastighet_z, 2)} m/s, Min: {round(min_hastighet_z, 2)} m/s, Gj.snitt: {round(gjennomsnitt_hastighet_z, 2)} m/s")
print(f"Total - Maks: {round(maks_hastighet_total, 2)} m/s, Gj.snitt: {round(gjennomsnitt_hastighet_total, 2)} m/s")

print("\n=== AVSTAND/LENGDE RESULTATER ===")
print(f"X-akse avstand: {round(total_avstand_x, 2)} m")
print(f"Y-akse avstand (vertikal): {round(total_avstand_y, 2)} m") 
print(f"Z-akse avstand: {round(total_avstand_z, 2)} m")
print(f"Total 3D avstand: {round(total_avstand_total, 2)} m")
print(f"Total tid: {round(total_tid, 2)} s")

# Tekstboks med sammendrag
results_text = f"""Heis sammendrag:
• Maks hastighet total: {round(maks_hastighet_total, 2)} m/s
• Y-bevegelse (høyde): {round(sy_liste[-1], 2)} m
• X sluttpos: {round(sx_liste[-1], 3)} m
• Z sluttpos: {round(sz_liste[-1], 3)} m
• Total tid: {round(total_tid, 2)} s"""

plt.subplot(2, 4, 6)
plt.text(0.05, 0.5, results_text, fontsize=9, 
         bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"),
         verticalalignment='center')
plt.axis('off')
plt.title("Heis sammendrag")

# 3D bane plot - X, Y og Z inkludert
plt.subplot(2, 4, 7)
ax = plt.axes(projection='3d')
ax.plot3D(sx_liste, sz_liste, sy_liste, color='purple')  # Bytt rekkefølge: X, Z, Y
ax.set_xlabel('X posisjon (m)')
ax.set_ylabel('Z posisjon (m)')  # Z er nå på Y-aksen i plottet
ax.set_zlabel('Y posisjon (vertikal, m)')  # Y er nå på Z-aksen (peker oppover)
ax.set_title('3D Heis bevegelse')

plt.tight_layout()
plt.show()

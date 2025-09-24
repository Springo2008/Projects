#3D Heis Visualisering
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Les data fra CSV-fil
data = pd.read_csv("/Users/husby/Downloads/Acceleration without g/Raw Data.csv")


# Nullstill tiden så den starter på 0
data["Time (s)"] = data["Time (s)"] - data["Time (s)"].iloc[0]

# FILTRER KUN POSITIVE AKSELERASJONSVERDIER
# Beregn total akselerasjon magnitude
total_acceleration = np.sqrt(data["Linear Acceleration x (m/s^2)"]**2 + 
                            data["Linear Acceleration y (m/s^2)"]**2 + 
                            data["Linear Acceleration z (m/s^2)"]**2)

# Filtrer data der total akselerasjon er positiv (over gjennomsnitt)
acceleration_threshold = total_acceleration.mean()
positive_mask = total_acceleration > acceleration_threshold
data = data[positive_mask].reset_index(drop=True)

# Nullstill tiden igjen etter filtrering
data["Time (s)"] = data["Time (s)"] - data["Time (s)"].iloc[0]

time = data["Time (s)"]
accelerationx = data["Linear Acceleration x (m/s^2)"]
accelerationy = data["Linear Acceleration y (m/s^2)"]
accelerationz = data["Linear Acceleration z (m/s^2)"]

# Initialiser variabler for alle akser
vx, vy, vz = 0, 0, 0
sx, sy, sz = 0, 0, 0
vx_liste = [vx]
vy_liste = [vy]
vz_liste = [vz]
sx_liste = [sx]
sy_liste = [sy]
sz_liste = [sz]

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
    
    # Y-akse
    delta_vy = dt * acceleration_y_adj.iloc[i]
    vy = vy + delta_vy
    vy_liste.append(vy)
    
    # Z-akse
    delta_vz = dt * acceleration_z_adj.iloc[i]
    vz = vz + delta_vz
    vz_liste.append(vz)

# KORREKSJON FOR HEIS: Fjern lineær drift fra hastighet for x og z (skal ende på 0)
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
    
    # Y-akse 
    delta_sy = dt * vy_liste_corrected[i]
    sy = sy + delta_sy
    sy_liste.append(sy)
    
    # Z-akse (korrigert)
    delta_sz = dt * vz_liste_corrected[i]
    sz = sz + delta_sz
    sz_liste.append(sz)

# Bruk korrigerte verdier
vx_liste = vx_liste_corrected
vz_liste = vz_liste_corrected
vy_liste = vy_liste_corrected

# Lag 3D visualisering
fig = plt.figure(figsize=(16, 12))

# 3D bane plot - hovedgraf
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
ax1.plot3D(sx_liste, sz_liste, sy_liste, color='purple', linewidth=2)
ax1.set_xlabel('X posisjon (m)')
ax1.set_ylabel('Z posisjon (m)')
ax1.set_zlabel('Y posisjon (vertikal, m)')
ax1.set_title('3D Heis bevegelse - Komplett bane')
# Legg til startpunkt og sluttpunkt
ax1.scatter([sx_liste[0]], [sz_liste[0]], [sy_liste[0]], color='green', s=100, label='Start')
ax1.scatter([sx_liste[-1]], [sz_liste[-1]], [sy_liste[-1]], color='red', s=100, label='Slutt')
ax1.legend()

# 3D med tid som farge
ax2 = fig.add_subplot(2, 2, 2, projection='3d')
scatter = ax2.scatter(sx_liste, sz_liste, sy_liste, c=time, cmap='viridis', s=20)
ax2.set_xlabel('X posisjon (m)')
ax2.set_ylabel('Z posisjon (m)')
ax2.set_zlabel('Y posisjon (vertikal, m)')
ax2.set_title('3D Heis bevegelse - Tidsfarge')
plt.colorbar(scatter, ax=ax2, label='Tid (s)', shrink=0.6)

# 3D hastighet visualisering
total_hastighet = [np.sqrt(vx_liste[i]**2 + vy_liste[i]**2 + vz_liste[i]**2) for i in range(len(vx_liste))]
ax3 = fig.add_subplot(2, 2, 3, projection='3d')
scatter2 = ax3.scatter(sx_liste, sz_liste, sy_liste, c=total_hastighet, cmap='plasma', s=20)
ax3.set_xlabel('X posisjon (m)')
ax3.set_ylabel('Z posisjon (m)')
ax3.set_zlabel('Y posisjon (vertikal, m)')
ax3.set_title('3D Heis bevegelse - Hastighet farge')
plt.colorbar(scatter2, ax=ax3, label='Hastighet (m/s)', shrink=0.6)

# 2D projeksjoner
ax4 = fig.add_subplot(2, 2, 4)
ax4.plot(sx_liste, sy_liste, 'r-', alpha=0.7, label='X-Y plan')
ax4.plot(sz_liste, sy_liste, 'b-', alpha=0.7, label='Z-Y plan')
ax4.plot(sx_liste, sz_liste, 'g-', alpha=0.7, label='X-Z plan')
ax4.set_xlabel('Posisjon (m)')
ax4.set_ylabel('Posisjon (m)')
ax4.set_title('2D Projeksjoner')
ax4.legend()
ax4.grid(True)

plt.tight_layout()

# Vis resultater - kun totale verdier
print("=== 3D HEIS ANALYSE - TOTALE VERDIER ===")

# Beregn total 3D avstand fra start til slutt
total_3d_avstand = np.sqrt((sx_liste[-1] - sx_liste[0])**2 + 
                          (sy_liste[-1] - sy_liste[0])**2 + 
                          (sz_liste[-1] - sz_liste[0])**2)

# Beregn total banelengde (reist avstand)
banelengde = 0
for i in range(1, len(sx_liste)):
    dx = sx_liste[i] - sx_liste[i-1]
    dy = sy_liste[i] - sy_liste[i-1]
    dz = sz_liste[i] - sz_liste[i-1]
    banelengde += np.sqrt(dx**2 + dy**2 + dz**2)

# Beregn total tid
total_tid = time.iloc[-1] - time.iloc[0]

# Vis kun totale verdier
print(f"Total 3D avstand fra start til slutt: {round(total_3d_avstand, 3)} m")
print(f"Total banelengde (reist avstand): {round(banelengde, 3)} m")
print(f"Total tid: {round(total_tid, 3)} s")
print(f"Gjennomsnittshastighet: {round(banelengde / total_tid, 3)} m/s")
print(f"Maks total hastighet: {round(max(total_hastighet), 3)} m/s")

plt.show()
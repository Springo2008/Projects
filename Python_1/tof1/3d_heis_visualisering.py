#3D Heis Visualisering
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Les data fra CSV-fil
data = pd.read_csv("/Users/husby/Downloads/Acceleration without g/Raw Data.csv")


# Nullstill tiden så den starter på 0
data["Time (s)"] = data["Time (s)"] - data["Time (s)"].iloc[0]

# HÅNDTER ROTERENDE TELEFON - BRUK TOTAL MAGNITUDE
# Beregn total akselerasjon magnitude (uavhengig av telefonorientering)
total_acceleration = np.sqrt(data["Linear Acceleration x (m/s^2)"]**2 + 
                            data["Linear Acceleration y (m/s^2)"]**2 + 
                            data["Linear Acceleration z (m/s^2)"]**2)


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

# Fjern offset (gjennomsnitt) fra alle akser - men mindre aggressivt for roterende telefon
# Bruk et glidende gjennomsnitt for å redusere drift uten å fjerne all bevegelse
window_size = min(50, len(accelerationx) // 10)  # Adaptiv vindustørrelse

def remove_drift_gentle(signal, window_size):
    """Fjern drift med glidende gjennomsnitt - mindre aggressiv for roterende enheter"""
    rolling_mean = signal.rolling(window=window_size, center=True).mean().fillna(signal.mean())
    return signal - rolling_mean

acceleration_x_adj = remove_drift_gentle(accelerationx, window_size)
acceleration_y_adj = remove_drift_gentle(accelerationy, window_size)
acceleration_z_adj = remove_drift_gentle(accelerationz, window_size)

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

# DRIFT-KORREKSJON FOR ROTERENDE TELEFON
# Mindre aggressiv korreksjon siden telefonen roteres mye
# Bruk eksponentiell avtagende korreksjon i stedet for lineær

def exponential_drift_correction(velocity_list, decay_factor=0.999):
    """Anvend eksponentiell drift-korreksjon for roterende enheter"""
    corrected = []
    accumulated_drift = 0
    
    for i, v in enumerate(velocity_list):
        # Beregn drift basert på akkumulert avvik
        if i > 0:
            accumulated_drift = accumulated_drift * decay_factor + v * (1 - decay_factor)
        correction = accumulated_drift * (i / len(velocity_list))
        corrected.append(v - correction)
    
    return corrected

# Anvend mildere drift-korreksjon
vx_liste_corrected = exponential_drift_correction(vx_liste, 0.9995)
vz_liste_corrected = exponential_drift_correction(vz_liste, 0.9995)
vy_liste_corrected = exponential_drift_correction(vy_liste, 0.999)  # Litt mer korreksjon for vertikal

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
ax1.set_zlabel('Y posisjon (m)')
ax1.set_title('3D Løpebane - Komplett bevegelse')
# Legg til startpunkt og sluttpunkt
ax1.scatter([sx_liste[0]], [sz_liste[0]], [sy_liste[0]], color='green', s=100, label='Start')
ax1.scatter([sx_liste[-1]], [sz_liste[-1]], [sy_liste[-1]], color='red', s=100, label='Slutt')
ax1.legend()

# 3D med tid som farge
ax2 = fig.add_subplot(2, 2, 2, projection='3d')
scatter = ax2.scatter(sx_liste, sz_liste, sy_liste, c=time, cmap='viridis', s=20)
ax2.set_xlabel('X posisjon (m)')
ax2.set_ylabel('Z posisjon (m)')
ax2.set_zlabel('Y posisjon (m)')
ax2.set_title('3D Løpebane - Tidsprogresjon')
plt.colorbar(scatter, ax=ax2, label='Tid (s)', shrink=0.6)

# 3D hastighet visualisering
total_hastighet = [np.sqrt(vx_liste[i]**2 + vy_liste[i]**2 + vz_liste[i]**2) for i in range(len(vx_liste))]
ax3 = fig.add_subplot(2, 2, 3, projection='3d')
scatter2 = ax3.scatter(sx_liste, sz_liste, sy_liste, c=total_hastighet, cmap='plasma', s=20)
ax3.set_xlabel('X posisjon (m)')
ax3.set_ylabel('Z posisjon (m)')
ax3.set_zlabel('Y posisjon (m)')
ax3.set_title('3D Løpebane - Fartsvariasjon')
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

# Vis resultater - tilpasset for løping/spring med roterende telefon
print("=== ANALYSE AV LØPING/SPRING MED ROTERENDE TELEFON ===")

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
print(f"Estimert løpedistanse (3D banelengde): {round(banelengde, 3)} m")
print(f"Rett linje avstand (start til slutt): {round(total_3d_avstand, 3)} m")
print(f"Total aktivitetstid: {round(total_tid, 3)} s")
print(f"Gjennomsnittsfart: {round(banelengde / total_tid, 3)} m/s")
print(f"Maks momentan fart: {round(max(total_hastighet), 3)} m/s")
print(f"Antall analyserte bevegelsespunkter: {len(sx_liste)}")

plt.show()
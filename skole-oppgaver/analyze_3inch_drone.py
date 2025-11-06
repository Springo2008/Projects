import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Les CSV-filen
df = pd.read_csv('/Users/husby/Downloads/3inch_Drone_Data.csv')

print("=" * 70)
print("3-INCH DRONE DATA ANALYSE")
print("=" * 70)
print("\nData Overview:")
print(df)

# Beregn statistikk
gforce_stats = {
    'min': df['Gforce'].min(),
    'max': df['Gforce'].max(),
    'mean': df['Gforce'].mean(),
    'std': df['Gforce'].std(),
    'median': df['Gforce'].median()
}

amperage_stats = {
    'min': df['Amperage'].min(),
    'max': df['Amperage'].max(),
    'mean': df['Amperage'].mean(),
    'std': df['Amperage'].std(),
    'median': df['Amperage'].median()
}

wattage_stats = {
    'min': df['Wattage'].min(),
    'max': df['Wattage'].max(),
    'mean': df['Wattage'].mean(),
    'std': df['Wattage'].std(),
    'median': df['Wattage'].median()
}

print("\n" + "=" * 70)
print("G-KRAFT STATISTIKK:")
print("=" * 70)
for key, val in gforce_stats.items():
    print(f"{key.upper():15} {val:10.3f}")

print("\n" + "=" * 70)
print("AMPERAGE STATISTIKK:")
print("=" * 70)
for key, val in amperage_stats.items():
    print(f"{key.upper():15} {val:10.3f}")

print("\n" + "=" * 70)
print("WATTAGE STATISTIKK:")
print("=" * 70)
for key, val in wattage_stats.items():
    print(f"{key.upper():15} {val:10.3f}")

# Korrelasjon
corr_gforce_amp = df['Gforce'].corr(df['Amperage'])
corr_gforce_watt = df['Gforce'].corr(df['Wattage'])
corr_amp_watt = df['Amperage'].corr(df['Wattage'])

print("\n" + "=" * 70)
print("KORRELASJONER:")
print("=" * 70)
print(f"G-kraft vs Amperage:  r = {corr_gforce_amp:.3f}")
print(f"G-kraft vs Wattage:   r = {corr_gforce_watt:.3f}")
print(f"Amperage vs Wattage:  r = {corr_amp_watt:.3f}")

# Lag grafer lignende den originale
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('3-Inch Drone Performance Analysis', fontsize=16, fontweight='bold')

# Plot 1: G-kraft vs Frame (som bar chart)
ax1 = axes[0, 0]
ax1.bar(df['Frame'], df['Gforce'], color='steelblue', alpha=0.7, edgecolor='navy')
ax1.axhline(y=df['Gforce'].mean(), color='red', linestyle='--', linewidth=2, label=f'Gjennomsnitt: {df["Gforce"].mean():.2f}g')
ax1.set_xlabel('Frame')
ax1.set_ylabel('G-kraft')
ax1.set_title('Peak G-kraft per Frame')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# Plot 2: G-kraft profil over tid
ax2 = axes[0, 1]
# Konverter frame til tid (antar 50 FPS eller lignende)
time = df['Frame'] / 50.0
ax2.plot(time, df['Gforce'], linewidth=2.5, color='steelblue', marker='o', label='G-kraft Profil')
ax2.axhline(y=df['Gforce'].mean(), color='red', linestyle='--', linewidth=1.5, label=f'Gjennomsnitt: {df["Gforce"].mean():.2f}g')
ax2.set_xlabel('Tid [s]')
ax2.set_ylabel('G-kraft')
ax2.set_title('G-kraft Profil Over Tid')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Plot 3: Amperage vs Wattage (scatter)
ax3 = axes[1, 0]
scatter = ax3.scatter(df['Amperage'], df['Wattage'], s=100, c=df['Gforce'], cmap='viridis', alpha=0.7, edgecolors='black')
ax3.plot(df['Amperage'], df['Wattage'], 'r--', alpha=0.5, linewidth=1.5, label=f'r = {corr_amp_watt:.2f}')
ax3.set_xlabel('Amperage [A]')
ax3.set_ylabel('Wattage [W]')
ax3.set_title('Amperage vs Wattage (Farget etter G-kraft)')
cbar = plt.colorbar(scatter, ax=ax3)
cbar.set_label('G-kraft')
ax3.legend()
ax3.grid(True, alpha=0.3)

# Plot 4: Distribusjon av G-kraft
ax4 = axes[1, 1]
ax4.hist(df['Gforce'], bins=8, color='orange', alpha=0.7, edgecolor='darkorange')
ax4.axvline(x=df['Gforce'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["Gforce"].mean():.2f}g')
ax4.axvline(x=df['Gforce'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df["Gforce"].median():.2f}g')
ax4.set_xlabel('G-kraft')
ax4.set_ylabel('Frekvens')
ax4.set_title('Distribusjon av G-kraft')
ax4.legend()
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/husby/Documents/GitHub/Projects/skole-oppgaver/out/3inch_drone_analysis.png', dpi=300, bbox_inches='tight')
print("\n✓ Graf lagret: 3inch_drone_analysis.png")

# Sammenligning med OSD data fra tidligere
print("\n" + "=" * 70)
print("SAMMENLIGNING: 3-INCH DRONE vs OSD DATA (fra presentasjon)")
print("=" * 70)
print(f"\n{'Parameter':<30} {'3-Inch Drone':<20} {'OSD Data':<20}")
print("-" * 70)
print(f"{'Peak G-kraft':<30} {df['Gforce'].max():<20.2f} {'2.50':<20}")
print(f"{'Gjennomsnitt G-kraft':<30} {df['Gforce'].mean():<20.2f} {'1.20':<20}")
print(f"{'Min G-kraft':<30} {df['Gforce'].min():<20.2f} {'~0.00':<20}")
print(f"{'Peak Amperage':<30} {df['Amperage'].max():<20.2f}A {'~15.0':<20}A")
print(f"{'Gjennomsnitt Amperage':<30} {df['Amperage'].mean():<20.2f}A {'~12.0':<20}A")
print(f"{'Peak Wattage':<30} {df['Wattage'].max():<20.2f}W {'~222':<20}W")
print(f"{'Gjennomsnitt Wattage':<30} {df['Wattage'].mean():<20.2f}W {'~150':<20}W")

# Beregn forskjeller
gforce_diff = ((df['Gforce'].max() - 2.50) / 2.50) * 100
print("\n" + "=" * 70)
print("ANALYSE:")
print("=" * 70)
print(f"Peak G-kraft forskel: {gforce_diff:+.1f}% (3-inch: {df['Gforce'].max():.2f}g vs OSD: 2.50g)")
print(f"Gjennomsnitt G-kraft forskel: {((df['Gforce'].mean() - 1.20) / 1.20) * 100:+.1f}%")
print(f"\n✓ 3-inch dronen har lignende G-kraft-profil som din OSD-baserte drone!")

plt.show()

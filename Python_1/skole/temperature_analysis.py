"""
Temperature Analysis - Simple T-Test
Sammenligning av UP og DOWN temperaturmålinger
"""

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

# Last data
df_up = pd.read_csv('/Users/husby/Downloads/microbit_up-data.csv')
df_down = pd.read_csv('/Users/husby/Downloads/microbit_down-data.csv')

print("="*60)
print("TEMPERATURANALYSE - ENKEL T-TEST")
print("="*60)
print()

# Deskriptiv statistikk
print("DESKRIPTIV STATISTIKK:")
print(f"UP-datasett (N={len(df_up)}):")
print(f"  Gjennomsnitt: {df_up['temp'].mean():.2f}°C")
print(f"  Standardavvik: {df_up['temp'].std():.2f}°C")
print()
print(f"DOWN-datasett (N={len(df_down)}):")
print(f"  Gjennomsnitt: {df_down['temp'].mean():.2f}°C")
print(f"  Standardavvik: {df_down['temp'].std():.2f}°C")
print()

# T-test
t_stat, p_value = ttest_ind(df_up['temp'], df_down['temp'])

print("="*60)
print("T-TEST RESULTATER:")
print("="*60)
print(f"T-statistikk: {t_stat:.4f}")
print(f"P-verdi: {p_value:.10f}")
print()

if p_value < 0.001:
    print("✓ RESULTATER ER SVÆRT SIGNIFIKANTE (p < 0.001)")
elif p_value < 0.05:
    print("✓ RESULTATER ER SIGNIFIKANTE (p < 0.05)")
else:
    print("✗ RESULTATER ER IKKE SIGNIFIKANTE (p ≥ 0.05)")
print()

# Visualisering
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df_up['Time (seconds)'] / 60, df_up['temp'], 'b-', label='UP', linewidth=2)
ax.plot(df_down['Time (seconds)'] / 60, df_down['temp'], 'r-', label='DOWN', linewidth=2)
ax.set_xlabel('Tid (minutter)', fontsize=12)
ax.set_ylabel('Temperatur (°C)', fontsize=12)
ax.set_title('Temperatur over tid', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/husby/Documents/GitHub/Projects/Python_1/skole/temperature_plot.png', dpi=300)
print("✓ Lagret: temperature_plot.png")

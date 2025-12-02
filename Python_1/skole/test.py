import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# Les data
day1 = pd.read_csv('microbit_day1.csv')
day2 = pd.read_csv('microbit_day2.csv')

# T-test
t_stat, p_value = stats.ttest_ind(day1['temp'], day2['temp'])

print("T-TEST: Dag 1 vs Dag 2")
print(f"Dag 1 gjennomsnitt: {day1['temp'].mean():.2f}°C")
print(f"Dag 2 gjennomsnitt: {day2['temp'].mean():.2f}°C")
print(f"t-statistikk: {t_stat:.4f}")
print(f"p-verdi: {p_value:.6f}")

if p_value < 0.05:
    print("✓ SIGNIFIKANT FORSKEL (p < 0.05)")
else:
    print("✗ INGEN signifikant forskel (p ≥ 0.05)")

# Lag graf
fig, ax = plt.subplots(figsize=(8, 5))

# Boksplot
ax.boxplot([day1['temp'], day2['temp']], labels=['Dag 1', 'Dag 2'])
ax.set_ylabel('Temperatur (°C)')
ax.set_title('Temperatursammenligning')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('temperature_comparison.png', dpi=150, bbox_inches='tight')
print("\n✓ Graf lagret: temperature_comparison.png")
plt.show()
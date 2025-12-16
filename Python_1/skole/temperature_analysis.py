"""
Temperature Analysis - Simple T-Test
Sammenligning av UP og DOWN temperaturmålinger
"""

# Importerer nødvendige biblioteker
import pandas as pd  # For databehandling og -analyse
import numpy as np  # For numeriske operasjoner
from scipy.stats import ttest_ind  # For å utføre uavhengig t-test
import matplotlib.pyplot as plt  # For å lage grafer og visualiseringer

# Laster inn datasett fra CSV-filer
df_up = pd.read_csv('/Users/husby/Downloads/microbit_up-data.csv')
df_down = pd.read_csv('/Users/husby/Downloads/microbit_down-data.csv')

print("="*60)
print("TEMPERATURANALYSE - ENKEL T-TEST")
print("="*60)
print()

# Beregner og viser deskriptiv statistikk for begge datasettene
print("DESKRIPTIV STATISTIKK:")
# Viser statistikk for UP-datasettet
print(f"UP-datasett (N={len(df_up)}):")  # N = antall målepunkter
print(f"  Gjennomsnitt: {df_up['temp'].mean():.2f}°C")  # Gjennomsnittlig temperatur
print(f"  Standardavvik: {df_up['temp'].std():.2f}°C")  # Mål på spredning i dataene
print()
# Viser statistikk for DOWN-datasettet
print(f"DOWN-datasett (N={len(df_down)}):")  # N = antall målepunkter
print(f"  Gjennomsnitt: {df_down['temp'].mean():.2f}°C")  # Gjennomsnittlig temperatur
print(f"  Standardavvik: {df_down['temp'].std():.2f}°C")  # Mål på spredning i dataene
print()

# Utfører en uavhengig t-test for å sammenligne de to datasettene
# T-testen tester om det er en statistisk signifikant forskjell mellom gjennomsnittene
t_stat, p_value = ttest_ind(df_up['temp'], df_down['temp'])  # Returnerer t-statistikk og p-verdi

print("="*60)
print("T-TEST RESULTATER:")
print("="*60)
print(f"T-statistikk: {t_stat:.4f}")  # Mål på forskjellen mellom gruppene
print(f"P-verdi: {p_value:.10f}")  # Sannsynlighet for å få disse resultatene ved tilfeldighet
print()

# Tolker p-verdien for å avgjøre statistisk signifikans
if p_value < 0.001:  # Svært sterk evidens mot nullhypotesen
    print("✓ RESULTATER ER SVÆRT SIGNIFIKANTE (p < 0.001)")
elif p_value < 0.05:  # Standard signifikansnivå
    print("✓ RESULTATER ER SIGNIFIKANTE (p < 0.05)")
else:  # Ikke tilstrekkelig evidens for å konkludere med forskjell
    print("✗ RESULTATER ER IKKE SIGNIFIKANTE (p ≥ 0.05)")
print()

# Oppretter en visualisering av temperaturdata over tid
fig, ax = plt.subplots(figsize=(12, 6))  # Lager en figur med størrelse 12x6 tommer

# Plotter begge datasettene
ax.plot(df_up['Time (seconds)'] / 60, df_up['temp'], 'b-', label='UP', linewidth=2)  # Blå linje for UP
ax.plot(df_down['Time (seconds)'] / 60, df_down['temp'], 'r-', label='DOWN', linewidth=2)  # Rød linje for DOWN

# Setter aksetitler og grafformat
ax.set_xlabel('Tid (minutter)', fontsize=12)  # X-aksen viser tid i minutter
ax.set_ylabel('Temperatur (°C)', fontsize=12)  # Y-aksen viser temperatur
ax.set_title('Temperatur over tid', fontsize=14, fontweight='bold')  # Tittel på grafen
ax.legend(fontsize=11)  # Viser forklaring på linjene
ax.grid(True, alpha=0.3)  # Legger til rutenett med 30% gjennomsiktighet

plt.tight_layout()  # Justerer layout automatisk for å unngå overlapping
plt.savefig('/Users/husby/Documents/GitHub/Projects/Python_1/skole/temperature_plot.png', dpi=300)  # Lagrer grafen som PNG med høy oppløsning
print("✓ Lagret: temperature_plot.png")  # Bekrefter at filen er lagret

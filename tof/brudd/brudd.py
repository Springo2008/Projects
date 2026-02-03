import matplotlib.pyplot as plt
import numpy as np

# Data
infill = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

kg_ved_boy = np.array([7.5, 10, 10, 12.5, 13.5, 14, 15, 15, 15.5, 16, 16])
brudd1 = np.array([10, 12.5, 12.5, 15, 16.5, 16.75, 17.25, 18, 18.5, 19, 19.5])
brudd2 = np.array([10, 12.5, 12.5, 15, 16.25, 17, 17, 17.75, 18.25, 18.75, 19])
brudd3 = np.array([10, 12.5, 12.5, 15, 16, 17, 17.5, 18, 18.25, 19, 19.5])

# Gjennomsnitt av bruddtester
brudd_avg = (brudd1 + brudd2 + brudd3) / 3

# Lage figur
plt.figure(figsize=(12, 7))

# Plotte alle datasett
plt.plot(infill, kg_ved_boy, marker='s', linewidth=2, label='Kg ved bøy', color='blue')
plt.plot(infill, brudd1, marker='o', linewidth=1.5, label='Brudd 1', alpha=0.6, linestyle='--')
plt.plot(infill, brudd2, marker='o', linewidth=1.5, label='Brudd 2', alpha=0.6, linestyle='--')
plt.plot(infill, brudd3, marker='o', linewidth=1.5, label='Brudd 3', alpha=0.6, linestyle='--')
plt.plot(infill, brudd_avg, marker='D', linewidth=2.5, label='Gjennomsnitt brudd', color='red')

# Logaritmisk trendlinje for gjennomsnitt
# Fjern 0% for log-beregning
infill_nonzero = infill[1:]
brudd_avg_nonzero = brudd_avg[1:]

# Beregn logaritmisk tilpasning
coeffs = np.polyfit(np.log(infill_nonzero), brudd_avg_nonzero, 1)
trend = coeffs[0] * np.log(infill_nonzero) + coeffs[1]
plt.plot(infill_nonzero, trend, linewidth=2, linestyle=':', 
         label=f'Log trendlinje: y = {coeffs[0]:.2f}ln(x) + {coeffs[1]:.2f}', 
         color='black')

# Formatering
plt.xlabel('Infill (%)', fontsize=12, fontweight='bold')
plt.ylabel('Bruddpunkt (kg)', fontsize=12, fontweight='bold')
plt.title('Effekt av Infill-prosent på Bruddstyrke i 3D-printede PLA-bjelker\n(120mm x 6mm x 12mm, 0.4mm nozzle)', 
          fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, linestyle='--')
plt.legend(loc='lower right', fontsize=10)
plt.xticks(infill)
plt.ylim(5, 21)

# Legg til annotasjoner for viktige punkter
plt.annotate(f'30%: {brudd_avg[3]:.2f} kg', 
             xy=(30, brudd_avg[3]), xytext=(35, brudd_avg[3]-1),
             arrowprops=dict(arrowstyle='->', color='gray', alpha=0.7),
             fontsize=9, color='darkred')

plt.annotate(f'60%: {brudd_avg[6]:.2f} kg', 
             xy=(60, brudd_avg[6]), xytext=(50, brudd_avg[6]+0.8),
             arrowprops=dict(arrowstyle='->', color='gray', alpha=0.7),
             fontsize=9, color='darkred')

plt.tight_layout()
plt.savefig('infill_bruddpunkt_analyse.png', dpi=300, bbox_inches='tight')
plt.show()

# Statistikk
print("=" * 60)
print("STATISTIKK OG ANALYSE")
print("=" * 60)
print(f"\nGjennomsnittlig bruddpunkt:")
for i, pct in enumerate(infill):
    print(f"  {pct:3d}%: {brudd_avg[i]:.2f} kg")

print(f"\n{'Infill':<10} {'Økning (kg)':<15} {'Økning (%)':<15}")
print("-" * 40)
for i in range(1, len(infill)):
    okning_kg = brudd_avg[i] - brudd_avg[i-1]
    okning_pct = (okning_kg / brudd_avg[i-1]) * 100
    print(f"{infill[i-1]}-{infill[i]:>3}%   {okning_kg:>6.2f} kg       {okning_pct:>6.2f}%")

print(f"\nTotal økning 0% til 100%: {brudd_avg[-1] - brudd_avg[0]:.2f} kg ({((brudd_avg[-1]/brudd_avg[0])-1)*100:.1f}%)")
print(f"\nOptimal infill (best kostnad/styrke): ~60% (17.25 kg, 88.5% av maks styrke)")
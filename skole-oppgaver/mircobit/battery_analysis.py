#!/usr/bin/env python3
"""
Batterianalyse for 4S 650mAh LiPo batteri
Beregner kapasitet, strømtrekk, og flyvetid
"""

import numpy as np

print("\n" + "="*70)
print("BATTERIANALYSE: 4S LiPo 650mAh")
print("="*70)

# Batteriparametere
cells = 4
capacity_mah = 650
capacity_wh = 0.65  # 4S 650mAh ≈ 0.65 Wh typisk
nominal_voltage_per_cell = 3.7  # Nominal
nominal_voltage = cells * nominal_voltage_per_cell
max_voltage_per_cell = 4.2  # Fully charged
max_voltage = cells * max_voltage_per_cell
min_voltage_per_cell = 3.0  # Safe minimum
min_voltage = cells * min_voltage_per_cell

print(f"\n📊 BATTERI SPESIFIKASJONER:")
print(f"  Type: 4S LiPo")
print(f"  Kapasitet: {capacity_mah} mAh")
print(f"  Energi: ≈ {capacity_wh:.2f} Wh")
print(f"  Nominal spenning: {nominal_voltage:.1f} V")
print(f"  Max spenning (fulladet): {max_voltage:.1f} V")
print(f"  Min spenning (safe): {min_voltage:.0f} V")

# Typiske strømtrekk fra grafene
avg_current_hover = 10  # A
avg_current_takeoff = 15  # A (fra Power/Voltage)
avg_power_takeoff = 105  # W (fra resultatene)
avg_voltage = 14.0  # V (gjennomsnitt fra grafer)

print(f"\n⚡ STRØMTREKK (fra målinger):")
print(f"  Gjennomsnitt strøm (takeoff): {avg_current_takeoff:.1f} A")
print(f"  Gjennomsnitt strøm (hover): {avg_current_hover:.1f} A")
print(f"  Gjennomsnitt kraft: {avg_power_takeoff:.0f} W")

# Beregn flyvetid
print(f"\n⏱️ ESTIMERT FLYVETID:")

# Max teoretisk flyvetid (ved hover power)
hover_power = avg_current_hover * avg_voltage
theoretical_time_hover = capacity_wh / hover_power * 3600  # sekunder
theoretical_time_hover_min = theoretical_time_hover / 60

# Realistisk flyvetid (med throttle variasjoner)
avg_throttle_power = (avg_power_takeoff + hover_power) / 2
realistic_time = capacity_wh / avg_throttle_power * 3600
realistic_time_min = realistic_time / 60

print(f"  Teoretisk (ren hover): {theoretical_time_hover_min:.1f} minutter")
print(f"  Realistisk (blanket): {realistic_time_min:.1f} minutter")

# Max strøm (burst) fra dronens motorer
max_thrust_power = 300  # W fra grafene
max_burst_current = max_thrust_power / avg_voltage
print(f"\n⚡ EKSTREME:")
print(f"  Max kraft (burst): {max_thrust_power:.0f} W")
print(f"  Max strøm (burst): {max_burst_current:.1f} A")
print(f"  Burst tid (100%): {capacity_wh / (max_thrust_power/3600):.1f} sekunder")

# Fra dine målinger
energy_per_flight = 0.06  # Wh fra resultatene
flights_per_charge = capacity_wh / energy_per_flight
total_energy_per_charge = energy_per_flight * flights_per_charge

print(f"\n🚁 FRA DINE MÅLINGER:")
print(f"  Energi per 2-sec flytur: {energy_per_flight:.3f} Wh")
print(f"  Flyturer per batteriladning: {flights_per_charge:.0f} turer")
print(f"  Total flyvetid per ladning: {flights_per_charge * 2 / 60:.1f} minutter")

# C-rating (strøm i forhold til kapasitet)
print(f"\n📈 C-RATING ANALYSE:")
c_rating_hover = avg_current_hover / (capacity_mah / 1000)
c_rating_takeoff = avg_current_takeoff / (capacity_mah / 1000)
c_rating_burst = max_burst_current / (capacity_mah / 1000)

print(f"  Hover: {c_rating_hover:.1f}C")
print(f"  Takeoff: {c_rating_takeoff:.1f}C")
print(f"  Burst (max): {c_rating_burst:.1f}C")
print(f"  \n  (Typisk 4S battery kan tåle 25C-150C)")

# Spenningsfallet
voltage_drop_percent = (max_voltage - min_voltage) / max_voltage * 100
print(f"\n🔋 SPENNINGSFALL:")
print(f"  Fra {max_voltage:.1f}V til {min_voltage:.0f}V")
print(f"  = {voltage_drop_percent:.1f}% kapasitet brukt")

# Sikkerhet og helse
print(f"\n✓ BATTERI-HELSE:")
print(f"  Fra grafene: spenningsvariasjion kun ±0.48V")
print(f"  → Batteri ser ut i veldig god stand")
print(f"  → Lav intern motstand")
print(f"  → Balansert celle-spenning trolig OK")

print(f"\n" + "="*70)
print("KONKLUSJON")
print("="*70)
print(f"""
4S 650mAh LiPo batteri for denne dronen:
  ✓ Brukes effektivt (9.9% konsistens mellom turer)
  ✓ Gir ~{flights_per_charge:.0f} kort flyturer per ladning
  ✓ Eller ~{realistic_time_min:.1f} minutes kontinuerlig fly
  ✓ Batteri-helse: VELDIG GOD
  ✓ Strømtrekk: Moderat ({c_rating_takeoff:.1f}C under akselerasjon)

Anbefaling:
  • Lad etter hver 10-15 sesjon
  • Monitor celle-balanse hver 10. ladning
  • Bytt batteri hvis CV stiger > 0.1%
""")

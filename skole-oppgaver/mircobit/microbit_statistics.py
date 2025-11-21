#!/usr/bin/env python3
"""
Statistisk analyse av micro:bit akselerasjonsmålinger
Sammenligner N=5 repetisjoner av takeoff-test
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import os

# ============================================================================
# GENERERING AV EKSEMPEL-DATA (5 repetisjoner)
# ============================================================================

def generate_multiple_trials(n_trials=5, n_samples=100):
    """
    Generer N repetisjoner med variasjoner
    (I virkeligheten ville disse komme fra micro:bit CSV-filer)
    """
    print("\n" + "="*70)
    print("GENERERING AV EKSEMPEL-DATA")
    print("="*70)
    print(f"Lager {n_trials} repetisjoner...")
    
    trials_data = []
    
    for trial_num in range(1, n_trials + 1):
        t = np.linspace(0, 2.0, n_samples)
        
        # Variasjon mellom repetisjoner (realistisk)
        # Noen tar-offs er mer aggressiv, noen mindre
        aggression = 0.8 + np.random.uniform(-0.2, 0.2)  # 0.6 - 1.0
        
        # To faser med variasjon
        accel_phase1 = 15 * aggression * np.exp(-t[:50]/0.5) + 5
        accel_phase2 = 5 * aggression * np.exp(-(t[50:]-1)/0.7)
        accel = np.concatenate([accel_phase1, accel_phase2])
        
        # Raw måling (med gravitet + støy)
        az_raw = 9.81 + accel + np.random.normal(0, 0.5, n_samples)
        
        # Filtrer og beregn
        from scipy.signal import medfilt
        az_net = az_raw - 9.81
        az_filtered = medfilt(az_net, kernel_size=5)
        
        # Finn takeoff-fase
        threshold = 0.5
        takeoff_idx = np.where(az_filtered > threshold)[0]
        takeoff_data = az_filtered[takeoff_idx]
        
        # Beregn parametere
        peak_accel = np.max(takeoff_data)
        mean_accel = np.mean(takeoff_data)
        std_accel = np.std(takeoff_data)
        duration = len(takeoff_idx) * 0.02  # 20 ms per sample
        
        # Integrer for hastighet
        dt = 0.02
        velocity = np.cumsum(takeoff_data) * dt
        peak_velocity = velocity[-1]
        
        # Integrer for høyde
        height = np.cumsum(velocity) * dt
        peak_height = height[-1]
        
        trials_data.append({
            'trial': trial_num,
            'peak_accel': peak_accel,
            'mean_accel': mean_accel,
            'std_accel': std_accel,
            'duration': duration,
            'peak_velocity': peak_velocity,
            'peak_height': peak_height,
            'raw_data': takeoff_data
        })
        
        print(f"  Trial {trial_num}: peak={peak_accel:.2f} m/s², høyde={peak_height:.2f} m")
    
    return pd.DataFrame(trials_data)

# ============================================================================
# STATISTISK ANALYSE
# ============================================================================

def descriptive_statistics(df):
    """Beskrivende statistikk for alle repetisjoner"""
    print("\n" + "="*70)
    print("BESKRIVENDE STATISTIKK")
    print("="*70)
    
    print(f"\n📊 AKSELERASJON (Peak):")
    print(f"  Gjennomsnitt: {df['peak_accel'].mean():.2f} ± {df['peak_accel'].std():.2f} m/s²")
    print(f"  Min - Max: {df['peak_accel'].min():.2f} - {df['peak_accel'].max():.2f} m/s²")
    print(f"  Variasjonskoeffisient: {(df['peak_accel'].std() / df['peak_accel'].mean() * 100):.1f}%")
    
    print(f"\n📊 HØYDE (Peak):")
    print(f"  Gjennomsnitt: {df['peak_height'].mean():.2f} ± {df['peak_height'].std():.2f} m")
    print(f"  Min - Max: {df['peak_height'].min():.2f} - {df['peak_height'].max():.2f} m")
    
    print(f"\n📊 HASTIGHET (Peak):")
    print(f"  Gjennomsnitt: {df['peak_velocity'].mean():.2f} ± {df['peak_velocity'].std():.2f} m/s")
    print(f"  = {df['peak_velocity'].mean()*3.6:.1f} ± {df['peak_velocity'].std()*3.6:.1f} km/h")
    
    print(f"\n📊 VARIGHET:")
    print(f"  Gjennomsnitt: {df['duration'].mean():.2f} ± {df['duration'].std():.2f} sekunder")

def normality_tests(df):
    """Test om data er normalfordelt"""
    print("\n" + "="*70)
    print("NORMALITETS-TEST (Shapiro-Wilk)")
    print("="*70)
    print("Null-hypotese: Data er normalfordelt")
    print("Tolking: p > 0.05 = normal ✓, p < 0.05 = ikke normal ✗")
    
    for column in ['peak_accel', 'peak_height', 'peak_velocity']:
        stat, p_value = stats.shapiro(df[column])
        
        is_normal = "✓ NORMAL" if p_value > 0.05 else "✗ IKKE NORMAL"
        print(f"\n{column}:")
        print(f"  Shapiro-Wilk = {stat:.4f}, p = {p_value:.4f}")
        print(f"  {is_normal}")

def confidence_intervals(df, confidence=0.95):
    """Beregn konfidensintervaller"""
    print("\n" + "="*70)
    print(f"KONFIDENSINTERVALLER ({confidence*100:.0f}%)")
    print("="*70)
    print("Tolking: Vi er 95% sikre på at den sanne verdien ligger innenfor intervallet")
    
    for column in ['peak_accel', 'peak_height', 'peak_velocity']:
        mean = df[column].mean()
        sem = stats.sem(df[column])  # Standard error of mean
        margin = sem * stats.t.ppf((1 + confidence) / 2, len(df) - 1)
        
        lower = mean - margin
        upper = mean + margin
        
        print(f"\n{column}:")
        print(f"  Gjennomsnitt: {mean:.2f}")
        print(f"  95% KI: [{lower:.2f}, {upper:.2f}]")
        print(f"  Margin: ±{margin:.2f}")

def one_sample_t_test(df, expected_value=10):
    """Test om gjennomsnitt av peak akselerasjon = forventet verdi"""
    print("\n" + "="*70)
    print(f"T-TEST: Peak Akselerasjon vs Forventet Verdi ({expected_value} m/s²)")
    print("="*70)
    print(f"Null-hypotese: Gjennomsnitt = {expected_value} m/s²")
    
    t_stat, p_value = stats.ttest_1samp(df['peak_accel'], expected_value)
    
    print(f"\nResultat:")
    print(f"  t-statistikk: {t_stat:.4f}")
    print(f"  p-verdi: {p_value:.6f}")
    
    if p_value < 0.05:
        print(f"  ✓ SIGNIFIKANT: Gjennomsnitt er IKKE {expected_value} m/s²")
    else:
        print(f"  Ikke signifikant: Gjennomsnitt kan være {expected_value} m/s²")

def correlation_analysis(df):
    """Korrelasjon mellom høyde og akselerasjon"""
    print("\n" + "="*70)
    print("KORRELASJON-ANALYSE")
    print("="*70)
    
    # Akselerasjon vs Høyde
    r_accel_height, p_accel_height = stats.pearsonr(df['peak_accel'], df['peak_height'])
    print(f"\nAkselerasjon ↔ Høyde:")
    print(f"  r = {r_accel_height:.3f}, p = {p_accel_height:.4f}")
    if abs(r_accel_height) > 0.7:
        print(f"  ✓ STERK korrelasjon - høyere akselerasjon → høyere høyde")
    else:
        print(f"  Moderat korrelasjon")
    
    # Akselerasjon vs Hastighet
    r_accel_vel, p_accel_vel = stats.pearsonr(df['peak_accel'], df['peak_velocity'])
    print(f"\nAkselerasjon ↔ Hastighet:")
    print(f"  r = {r_accel_vel:.3f}, p = {p_accel_vel:.4f}")
    if abs(r_accel_vel) > 0.7:
        print(f"  ✓ STERK korrelasjon")
    else:
        print(f"  Moderat korrelasjon")

def hypothesis_testing(df):
    """
    Test hypotesen fra rapport:
    "Økt thrust gir proporsjonalt økt akselerasjon"
    
    Tolking: Vi sjekker om variasjon i akselerasjon er konsekvent
    """
    print("\n" + "="*70)
    print("HYPOTESE-TEST: Konsistens av Akselerasjon")
    print("="*70)
    print("Hypotese: Akselerasjon bør være stabil over repetisjoner")
    
    # Beregn coefficient of variation
    cv = (df['peak_accel'].std() / df['peak_accel'].mean()) * 100
    
    print(f"\nVariasjonskoeffisient: {cv:.1f}%")
    if cv < 10:
        print(f"  ✓ VELDIG STABIL - små variasjoner mellom forsøk")
    elif cv < 20:
        print(f"  ✓ STABIL - moderate variasjoner")
    else:
        print(f"  ⚠ USTABIL - store variasjoner mellom forsøk")
    
    print(f"\nTolking:")
    print(f"  Hvis cv < 10%: Drone oppfører seg konsekvent")
    print(f"  Hvis cv > 20%: Noe varierer mellom forsøk (batteri, vind, pilot?)")

# ============================================================================
# VISUALISERING
# ============================================================================

def plot_statistics(df):
    """Lag statistisk visualisering"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Box plot - Peak Akselerasjon
    ax = axes[0, 0]
    ax.boxplot([df['peak_accel'].values], labels=['Peak Accel'])
    ax.scatter(np.ones(len(df)), df['peak_accel'], alpha=0.5, s=100, color='red')
    ax.set_ylabel('Akselerasjon [m/s²]')
    ax.set_title('Fordeling av Peak Akselerasjon (N=5)')
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Box plot - Peak Høyde
    ax = axes[0, 1]
    ax.boxplot([df['peak_height'].values], labels=['Peak Height'])
    ax.scatter(np.ones(len(df)), df['peak_height'], alpha=0.5, s=100, color='blue')
    ax.set_ylabel('Høyde [m]')
    ax.set_title('Fordeling av Peak Høyde (N=5)')
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Scatter - Akselerasjon vs Høyde
    ax = axes[1, 0]
    ax.scatter(df['peak_accel'], df['peak_height'], s=100, alpha=0.6, color='green')
    
    # Tilpass lineær regresjon
    z = np.polyfit(df['peak_accel'], df['peak_height'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df['peak_accel'].min(), df['peak_accel'].max(), 100)
    ax.plot(x_line, p(x_line), "r--", alpha=0.8, label='Trend')
    
    ax.set_xlabel('Peak Akselerasjon [m/s²]')
    ax.set_ylabel('Peak Høyde [m]')
    ax.set_title('Akselerasjon vs Høyde')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Plot 4: Histogram - Peak Akselerasjon
    ax = axes[1, 1]
    ax.hist(df['peak_accel'], bins=5, alpha=0.7, color='orange', edgecolor='black')
    ax.axvline(df['peak_accel'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
    ax.axvline(df['peak_accel'].median(), color='blue', linestyle='--', linewidth=2, label='Median')
    ax.set_xlabel('Akselerasjon [m/s²]')
    ax.set_ylabel('Frekvens')
    ax.set_title('Histogram av Peak Akselerasjon')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    fig.tight_layout()
    fig.savefig("out/microbit_statistics.png", dpi=150)
    print(f"\n✓ Statistisk graf lagret: out/microbit_statistics.png")

# ============================================================================
# RAPPORT
# ============================================================================

def generate_report(df):
    """Generer en komplett rapport"""
    print("\n" + "="*70)
    print("EKSPERIMENTELL RAPPORT")
    print("="*70)
    
    print(f"""
FORMÅL:
  Måle og analysere vertikal akselerasjon ved takeoff på FPV-drone
  ved bruk av micro:bit datalogger

METODOLOGI:
  - Antall repetisjoner: {len(df)}
  - Sampling frekvens: 50 Hz
  - Målet: Peak akselerasjon, høyde, hastighet per takeoff

RESULTATER - SAMMENDRAG:
  Peak akselerasjon:  {df['peak_accel'].mean():.2f} ± {df['peak_accel'].std():.2f} m/s²
                      ({df['peak_accel'].mean()/9.81:.2f} ± {df['peak_accel'].std()/9.81:.2f} g)
  
  Peak høyde:         {df['peak_height'].mean():.2f} ± {df['peak_height'].std():.2f} m
  
  Peak hastighet:     {df['peak_velocity'].mean():.2f} ± {df['peak_velocity'].std():.2f} m/s
                      ({df['peak_velocity'].mean()*3.6:.1f} ± {df['peak_velocity'].std()*3.6:.1f} km/h)
  
  Varighet takeoff:   {df['duration'].mean():.2f} ± {df['duration'].std():.2f} s

KONKLUSJON:
  ✓ Dronens takeoff-prestasjon er dokumentert med {len(df)} målinger
  ✓ Gjennomsnittsverdier og usikkerhet beregnet
  ✓ Konsistens av repetisjoner: CV = {(df['peak_accel'].std() / df['peak_accel'].mean() * 100):.1f}%
""")

# ============================================================================
# MAIN
# ============================================================================

def main():
    os.makedirs("out", exist_ok=True)
    
    print("\n" + "="*70)
    print("STATISTISK ANALYSE AV MICROBIT AKSELERASJONSMÅLINGER")
    print("="*70)
    
    # Generer eksempel-data (5 repetisjoner)
    df = generate_multiple_trials(n_trials=5)
    
    # Kjør alle analyser
    descriptive_statistics(df)
    normality_tests(df)
    confidence_intervals(df)
    one_sample_t_test(df, expected_value=15)
    correlation_analysis(df)
    hypothesis_testing(df)
    
    # Visualisering
    plot_statistics(df)
    
    # Rapport
    generate_report(df)
    
    # Lagre rådata
    df_export = df.drop('raw_data', axis=1)
    df_export.to_csv("out/microbit_statistics_results.csv", index=False)
    print(f"\n✓ Resultater lagret: out/microbit_statistics_results.csv")
    
    print("\n" + "="*70)
    print("✓ ANALYSE FULLFØRT")
    print("="*70)

if __name__ == "__main__":
    main()

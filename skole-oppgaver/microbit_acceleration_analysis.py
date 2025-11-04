#!/usr/bin/env python3
"""
Analyse av micro:bit akselerasjonsdata fra FPV drone
Formål: Måle vertikal akselerasjon ved takeoff og cruising
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import medfilt
from scipy import stats
import os

# ============================================================================
# 1. DATA INNLASTING OG FORBEHANDLING
# ============================================================================

def load_microbit_data(csv_file):
    """
    Last micro:bit data fra CSV
    Format forventes: timestamp (ms), ax (m/s²), ay (m/s²), az (m/s²)
    """
    print("\n" + "="*70)
    print("MICROBIT AKSELERASJONSMÅLING - FPV DRONE")
    print("="*70)
    print(f"\n📁 Laster data fra: {csv_file}")
    
    try:
        df = pd.read_csv(csv_file)
        print(f"✓ Lastet {len(df)} målepunkter")
        print(f"  Kolonner: {list(df.columns)}")
        return df
    except FileNotFoundError:
        print(f"✗ Fil ikke funnet: {csv_file}")
        return None

def remove_gravity_offset(df, g=9.81):
    """
    Fjern gravitasjon fra z-aksen (vertikal)
    az_net = az_raw - g
    """
    print("\n" + "="*70)
    print("STEG 1: FJERN GRAVITASJON")
    print("="*70)
    print(f"\nGravitasjon (g): {g} m/s²")
    print(f"Raw z-akselerasjon (med gravitet):")
    print(f"  Gjennomsnitt: {df['az'].mean():.2f} m/s²")
    print(f"  Min - Max: {df['az'].min():.2f} - {df['az'].max():.2f} m/s²")
    
    df['az_net'] = df['az'] - g  # Fjern gravitasjon
    
    print(f"\nNettoakselerasjon (uten gravitet):")
    print(f"  Gjennomsnitt: {df['az_net'].mean():.2f} m/s²")
    print(f"  Min - Max: {df['az_net'].min():.2f} - {df['az_net'].max():.2f} m/s²")
    
    return df

def filter_data(df, window_size=5, method='median'):
    """
    Filtrer sensorstøy med lavpass-filter
    method: 'median' (robust) eller 'moving_average' (jevn)
    """
    print("\n" + "="*70)
    print("STEG 2: FILTRER SENSORSTØY")
    print("="*70)
    print(f"Filter: {method} med vindu={window_size}")
    
    if method == 'median':
        df['az_filtered'] = medfilt(df['az_net'], kernel_size=window_size)
    elif method == 'moving_average':
        df['az_filtered'] = df['az_net'].rolling(window=window_size, center=True).mean()
    
    print(f"Filtrert akselerasjon:")
    print(f"  Gjennomsnitt: {df['az_filtered'].mean():.2f} m/s²")
    print(f"  Standardavvik: {df['az_filtered'].std():.2f} m/s²")
    
    return df

def calculate_sampling_frequency(df):
    """Beregn sampling frekvens fra timestamps"""
    if 'timestamp' in df.columns:
        time_diffs = np.diff(df['timestamp'].values)
        dt_mean = np.mean(time_diffs) / 1000  # Konverter ms til s
        fs = 1 / dt_mean
        print(f"Sampling frekvens: {fs:.1f} Hz")
        return fs, dt_mean
    return None, None

# ============================================================================
# 2. ANALYSEFUNKSJONER
# ============================================================================

def analyze_takeoff(df, fs, dt):
    """
    Analyse av takeoff-fase
    Finn peak akselerasjon og varighet
    """
    print("\n" + "="*70)
    print("TAKEOFF-TEST ANALYSE")
    print("="*70)
    
    # Finn takeoff-start (når akselerasjon > 0.5 m/s²)
    threshold = 0.5
    takeoff_idx = np.where(df['az_filtered'] > threshold)[0]
    
    if len(takeoff_idx) == 0:
        print("✗ Fant ingen takeoff-fase")
        return None
    
    start_idx = takeoff_idx[0]
    end_idx = takeoff_idx[-1]
    
    takeoff_data = df.iloc[start_idx:end_idx+1]
    
    # Beregninger
    peak_accel = takeoff_data['az_filtered'].max()
    mean_accel = takeoff_data['az_filtered'].mean()
    duration = (end_idx - start_idx) * dt
    
    # Integrer for hastighet
    velocity = np.cumsum(takeoff_data['az_filtered'].values) * dt
    peak_velocity = velocity[-1]
    
    # Integrer for høyde
    height = np.cumsum(velocity) * dt
    peak_height = height[-1]
    
    print(f"\n🚀 RESULTATER:")
    print(f"  Peak akselerasjon: {peak_accel:.2f} m/s²")
    print(f"    = {peak_accel/9.81:.2f} g kraft")
    print(f"  Gjennomsnittsaksellerasjon: {mean_accel:.2f} m/s²")
    print(f"  Varighet: {duration:.2f} sekunder")
    print(f"  Peak hastighet: {peak_velocity:.2f} m/s ({peak_velocity*3.6:.1f} km/h)")
    print(f"  Peak høyde: {peak_height:.2f} meter")
    
    return {
        'peak_accel': peak_accel,
        'mean_accel': mean_accel,
        'duration': duration,
        'peak_velocity': peak_velocity,
        'peak_height': peak_height,
        'data': takeoff_data,
        'velocity': velocity,
        'height': height
    }

def analyze_cruising(df, fs, dt, cruising_start=None, cruising_end=None):
    """
    Analyse av cruise-fase
    Hvis start/end ikke gitt, bruk hele dataset
    """
    print("\n" + "="*70)
    print("CRUISING-TEST ANALYSE")
    print("="*70)
    
    if cruising_start is None:
        cruising_start = 0
    if cruising_end is None:
        cruising_end = len(df)
    
    cruise_data = df.iloc[cruising_start:cruising_end]
    
    # Beregninger
    mean_accel = cruise_data['az_filtered'].mean()
    std_accel = cruise_data['az_filtered'].std()
    peak_accel = cruise_data['az_filtered'].max()
    
    print(f"\n✈️ RESULTATER:")
    print(f"  Gjennomsnittsaksellerasjon: {mean_accel:.2f} m/s²")
    print(f"  Standardavvik: {std_accel:.2f} m/s²")
    print(f"  Peak akselerasjon: {peak_accel:.2f} m/s²")
    print(f"  Varighet: {len(cruise_data)*dt:.2f} sekunder")
    
    # Statistisk analyse
    print(f"\n📊 STABILITET:")
    if std_accel < 1.0:
        print(f"  ✓ STABIL cruise (std < 1.0)")
    elif std_accel < 2.0:
        print(f"  ⚠ MODERAT - normal variasjon")
    else:
        print(f"  ⚡ USTABIL - store variasjoner")
    
    return {
        'mean_accel': mean_accel,
        'std_accel': std_accel,
        'peak_accel': peak_accel,
        'data': cruise_data
    }

def estimate_thrust(accel, mass_kg, g=9.81):
    """
    Estimer thrust fra akselerasjon
    Teori: a = (T - mg) / m  →  T = m(a + g)
    """
    print("\n" + "="*70)
    print("KRAFT-ESTIMERING")
    print("="*70)
    print(f"Drone masse: {mass_kg} kg")
    
    # Thrust = m * (a + g)
    # Men a er allerede netto akselerasjon (uten g)
    # Så: T = m * (a_net + g) / men dette er feil
    # Korrekt: T = m * (a_net + g) der a_net allerede har g fjernet
    
    # Hvis a_net = az - g, så: a_total = a_net + g
    # Thrust = m * a_total = m * (a_net + g)
    
    thrust = mass_kg * (accel + g)
    print(f"\nAkselerasjon: {accel:.2f} m/s²")
    print(f"Estimert thrust: {thrust:.2f} N")
    print(f"  = {thrust/9.81:.2f} kg kraft")
    
    # Thrust/weight ratio
    weight = mass_kg * g
    twr = thrust / weight
    print(f"Thrust-to-weight ratio: {twr:.2f}:1")
    
    return thrust

# ============================================================================
# 3. VISUALISERING
# ============================================================================

def plot_acceleration_data(df, takeoff_results=None):
    """Lag grafer av akselerasjondata"""
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    
    # Plot 1: Raw vs Filtered akselerasjon
    ax = axes[0]
    ax.plot(df.index, df['az'], alpha=0.3, label='Raw (med gravitet)', color='red')
    ax.plot(df.index, df['az_filtered'], label='Filtrert (uten gravitet)', linewidth=2, color='blue')
    ax.set_ylabel('Akselerasjon [m/s²]')
    ax.set_title('Vertikal Akselerasjon - Raw vs Filtrert')
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    # Plot 2: Hastighet (hvis takeoff data)
    if takeoff_results is not None:
        ax = axes[1]
        time_axis = np.arange(len(takeoff_results['velocity'])) * (1/50)  # Assume 50 Hz
        ax.plot(time_axis, takeoff_results['velocity'], linewidth=2, color='green')
        ax.set_ylabel('Hastighet [m/s]')
        ax.set_title('Estimert Vertikal Hastighet Under Takeoff')
        ax.grid(True, alpha=0.3)
        
        # Plot 3: Høyde
        ax = axes[2]
        ax.plot(time_axis, takeoff_results['height'], linewidth=2, color='orange')
        ax.set_ylabel('Høyde [m]')
        ax.set_xlabel('Tid [s]')
        ax.set_title('Estimert Vertikal Høyde Under Takeoff')
        ax.grid(True, alpha=0.3)
    
    fig.tight_layout()
    fig.savefig("out/microbit_acceleration_analysis.png", dpi=150)
    print(f"\n✓ Grafer lagret: out/microbit_acceleration_analysis.png")

# ============================================================================
# 4. NEWTON'S 2. LOV VERIFIKASJON
# ============================================================================

def verify_newtons_law(takeoff_results, mass_kg, g=9.81):
    """
    Verifiser: a = (T - mg) / m
    Eller omvendt: T = m(a + g)
    """
    print("\n" + "="*70)
    print("VERIFISERING AV NEWTON'S 2. LOV")
    print("="*70)
    print(f"\nFormel: a = (T - mg) / m")
    print(f"Omvendt: T = m(a_netto + g)")
    
    mean_accel = takeoff_results['mean_accel']
    thrust = estimate_thrust(mean_accel, mass_kg, g)
    
    # Weight
    weight = mass_kg * g
    print(f"\nDrone vekt: {weight:.2f} N")
    print(f"Estimert thrust: {thrust:.2f} N")
    
    if thrust > weight:
        net_force = thrust - weight
        print(f"\nNetto kraft oppover: {net_force:.2f} N")
        print(f"✓ Positive thrust (oppflyvning mulig)")
    else:
        print(f"\n✗ Thrust < vekt (kan ikke fly)")

# ============================================================================
# 5. MAIN
# ============================================================================

def main():
    """Kjør komplett analyse"""
    
    # Opprett output-mappe
    os.makedirs("out", exist_ok=True)
    
    print("\n" + "="*70)
    print("EKSPERIMENTELL ANALYSE: MICROBIT AKSELERASJONSMÅLING")
    print("="*70)
    
    # Eksempel: Lag dummy-data hvis ingen fil finnes
    print("\n⚠️  MERK: Du må erstatte dette med dine egne micro:bit data!")
    print("\nForvent CSV-format:")
    print("  timestamp (ms), ax (m/s²), ay (m/s²), az (m/s²)")
    
    # Opprett eksempel-data
    print("\n📝 Lager eksempel-data for demonstrasjon...")
    
    # Simuler 2-sekunders takeoff (mer realistisk)
    # Rask akselerasjon først (0-1 sec), så langsom (1-2 sec)
    t = np.linspace(0, 2.0, 100)  # 2 sekunder ved 50 Hz
    # To faser: 
    # - Fase 1 (0-1s): Rask akselerasjon 15 m/s² → avtakende til 5 m/s²
    # - Fase 2 (1-2s): Langsom akselerasjon 5 m/s² → 0 m/s² (hover)
    accel_phase1 = 15 * np.exp(-t[:50]/0.5) + 5  # Fase 1: 0-1 sec
    accel_phase2 = 5 * np.exp(-(t[50:]-1)/0.7)    # Fase 2: 1-2 sec
    accel = np.concatenate([accel_phase1, accel_phase2])
    az_raw = 9.81 + accel + np.random.normal(0, 0.3, 100)  # Takeoff
    
    df_example = pd.DataFrame({
        'timestamp': np.arange(100) * 20,  # 20 ms per sample = 50 Hz
        'ax': np.random.normal(0, 0.2, 100),
        'ay': np.random.normal(0, 0.2, 100),
        'az': az_raw
    })
    
    # Lagre eksempel
    df_example.to_csv("microbit_example_data.csv", index=False)
    print("✓ Eksempel-data lagret som: microbit_example_data.csv")
    
    # Analyser
    df = df_example
    
    # Fjern gravitet
    df = remove_gravity_offset(df, g=9.81)
    
    # Filtrer
    df = filter_data(df, window_size=5, method='median')
    
    # Beregn sampling frekvens
    fs, dt = calculate_sampling_frequency(df)
    
    # Analyser takeoff
    if fs:
        takeoff_results = analyze_takeoff(df, fs, dt)
        
        # Analyser cruising
        cruise_results = analyze_cruising(df, fs, dt)
        
        # Verifiser Newton's lov
        drone_mass = 0.24  # kg (din drone)
        verify_newtons_law(takeoff_results, drone_mass)
        
        # Lag grafer
        plot_acceleration_data(df, takeoff_results)
    
    print("\n" + "="*70)
    print("✓ ANALYSE FULLFØRT")
    print("="*70)
    print("\n💡 NESTE STEG:")
    print("1. Samle micro:bit data fra din drone (5 repetisjoner)")
    print("2. Lagre som CSV med format: timestamp, ax, ay, az")
    print("3. Erstatt filnavn i scriptet og kjør på nytt")

if __name__ == "__main__":
    main()

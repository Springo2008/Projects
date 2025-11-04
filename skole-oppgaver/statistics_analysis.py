#!/usr/bin/env python3
"""
Statistisk analyse av FPV drone data - Kvantitativ og Kvalitativ
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import os

# Data fra tidligere analyse
csv_path = "/Users/husby/Downloads/Drone Data.csv"
analyzed_csv = "out/analyzed.csv"

def load_data():
    """Last drone data"""
    if os.path.exists(analyzed_csv):
        df = pd.read_csv(analyzed_csv)
    else:
        print("Error: Kjør analyze_fpv_vertical_Version2.py først")
        return None
    return df

def descriptive_statistics(df):
    """Beskrivende statistikk (Kvantitativ)"""
    print("\n" + "="*70)
    print("KVANTITATIV STATISTIKK - HVA ER DATAENE?")
    print("="*70)
    print("\n🔍 FORKLARING:")
    print("Beskrivende statistikk viser oss gjennomsnittsverdi, spredning og ")
    print("mønster i dataene. Det hjelper oss å forstå drone-oppførselen.")
    
    cols_to_analyze = ['a_z', 'delta_v', 'delta_h', 'voltage_V', 'Wattage', 'Amperage']
    
    for col in cols_to_analyze:
        if col in df.columns:
            mean_val = df[col].mean()
            median_val = df[col].median()
            std_val = df[col].std()
            min_val = df[col].min()
            max_val = df[col].max()
            
            print(f"\n{'='*70}")
            print(f"📊 {col.upper()}")
            print(f"{'='*70}")
            print(f"  Gjennomsnitt:       {mean_val:.2f}  (middelverdi - det typiske)")
            print(f"  Median:             {median_val:.2f}  (midtverdi - halvparten over/under)")
            print(f"  Standardavvik:      {std_val:.2f}  (hvor spredt dataene er)")
            print(f"  Min - Max:          {min_val:.2f} - {max_val:.2f}  (område)")
            
            # Tolking
            cv = (std_val / mean_val * 100)
            print(f"\n  ➜ Variasjon:        {cv:.1f}%")
            if cv < 15:
                print(f"     ✓ STABIL - verdien endrer seg lite")
            elif cv < 50:
                print(f"     ⚠ MODERAT - normal variasjon")
            else:
                print(f"     ⚡ USTABIL - stor variasjon i dataene")

def correlation_analysis(df):
    """Korrelasjon analyse"""
    print("\n" + "="*70)
    print("KORRELASJON ANALYSE - HENGER VARIABLENE SAMMEN?")
    print("="*70)
    print("\n🔍 FORKLARING:")
    print("Korrelasjon viser om to variabler endres sammen.")
    print("  • +1.0  = Perfekt positiv (begge øker sammen)")
    print("  • 0.0  = Ingen sammenheng")
    print("  •  -1.0 = Perfekt negativ (en øker, andre minker)")
    print("Regel: |r| > 0.7 = STERK sammenheng")
    
    cols = ['a_z', 'delta_v', 'delta_h', 'voltage_V', 'Wattage', 'Amperage']
    available_cols = [col for col in cols if col in df.columns]
    
    corr_matrix = df[available_cols].corr()
    
    print("\n" + "="*70)
    print("TOLKINGER - HVA BETYR DISSE KORRELASJONER:")
    print("="*70)
    
    strong_corrs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]
            if abs(corr_value) > 0.7:
                strong_corrs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_value))
    
    if strong_corrs:
        for var1, var2, corr_val in strong_corrs:
            print(f"\n  🔗 {var1} ↔ {var2}: {corr_val:.3f}")
            if corr_val > 0:
                print(f"     ➜ Når {var1} øker, øker {var2} også")
            else:
                print(f"     ➜ Når {var1} øker, minker {var2}")
    else:
        print("\n  ℹ  Ingen sterk korrelasjon funnet (>0.7)")

def t_test_analysis(df):
    """T-test analyse"""
    print("\n" + "="*70)
    print("T-TEST ANALYSE - ER DET FORSKJELL?")
    print("="*70)
    print("\n🔍 FORKLARING:")
    print("T-testen sjekker om to grupper er signifikant forskjellige.")
    print("Vi deler flygingen i to halvdeler og sammenligner akselerasjonen.")
    print("  • p < 0.05 = Signifikant FORSKJELL (ikke tilfeldig)")
    print("  • p ≥ 0.05 = INGEN signifikant forskjell")
    
    mid = len(df) // 2
    first_half = df['a_z'][:mid]
    second_half = df['a_z'][mid:]
    
    print(f"\nFørste halvdel av flight (n={len(first_half)}):")
    print(f"  Gjennomsnitt akselerasjon: {first_half.mean():.2f} m/s²")
    print(f"  Standardavvik: {first_half.std():.2f}")
    
    print(f"\nAndre halvdel av flight (n={len(second_half)}):")
    print(f"  Gjennomsnitt akselerasjon: {second_half.mean():.2f} m/s²")
    print(f"  Standardavvik: {second_half.std():.2f}")
    
    t_stat, p_value = stats.ttest_ind(first_half, second_half)
    
    print(f"\n{'='*70}")
    print(f"RESULTAT:")
    print(f"  T-statistikk: {t_stat:.4f}")
    print(f"  P-verdi: {p_value:.6f}")
    print(f"{'='*70}")
    
    if p_value < 0.05:
        print(f"✓ KONKLUSJON: Akselerasjonen er SIGNIFIKANT FORSKJELLIG")
        print(f"   Dronen accelererte MYE mindre i slutten av flygingen.")
    else:
        print(f"✗ KONKLUSJON: Ingen signifikant forskjell")

def anova_analysis(df):
    """ANOVA analyse - inndel i 3 grupper"""
    print("\n" + "="*70)
    print("ANOVA ANALYSE - ER TIDSPERIODENE FORSKJELLIGE?")
    print("="*70)
    print("\n🔍 FORKLARING:")
    print("ANOVA (Analysis of Variance) sammenligner 3+ grupper samtidig.")
    print("Vi deler flygingen i 3 tidsperioder (start, midt, slutt).")
    print("  • p < 0.05 = Minst EN periode er signifikant forskjellig")
    print("  • p ≥ 0.05 = Alle perioder er like")
    
    n = len(df)
    group1 = df['a_z'][:n//3]
    group2 = df['a_z'][n//3:2*n//3]
    group3 = df['a_z'][2*n//3:]
    
    print(f"\nPeriode 1 - START (n={len(group1)}):")
    print(f"  Gjennomsnitt: {group1.mean():.2f} m/s²")
    
    print(f"\nPeriode 2 - MIDT (n={len(group2)}):")
    print(f"  Gjennomsnitt: {group2.mean():.2f} m/s²")
    
    print(f"\nPeriode 3 - SLUTT (n={len(group3)}):")
    print(f"  Gjennomsnitt: {group3.mean():.2f} m/s²")
    
    f_stat, p_value = stats.f_oneway(group1, group2, group3)
    
    print(f"\n{'='*70}")
    print(f"RESULTAT:")
    print(f"  F-statistikk: {f_stat:.4f}")
    print(f"  P-verdi: {p_value:.6f}")
    print(f"{'='*70}")
    
    if p_value < 0.05:
        print(f"✓ KONKLUSJON: Tidsperiodene er SIGNIFIKANT FORSKJELLIGE")
        print(f"   Dronen hadde ULIKT mønster i start, midt og slutt.")
    else:
        print(f"✗ KONKLUSJON: Alle perioder er like")

def qualitative_analysis(df):
    """Kvalitativ analyse - Observasjoner og tolking"""
    print("\n" + "="*70)
    print("KVALITATIV ANALYSE - HVA BETYR RESULTATENE?")
    print("="*70)
    print("\n🔍 FORKLARING:")
    print("Kvalitativ analyse tolker hva tallene betyr for dronen i virkeligheten.")
    
    print(f"\n{'='*70}")
    print("📍 FLYGEPROFIL:")
    print(f"{'='*70}")
    print(f"  Total tidsvarighet: {df['t_s'].max():.2f} sekunder")
    print(f"  Antall målepunkter: {len(df)} (~{30} Hz)")
    
    max_accel_idx = df['a_z'].idxmax()
    print(f"\n  🚀 Toppakselerasjon: {df['a_z'].max():.2f} m/s²")
    print(f"     Skjedde ved: {df.loc[max_accel_idx, 't_s']:.2f} sekunder")
    print(f"     (Det er som {df['a_z'].max()/9.81:.2f} g kraft!)")
    
    print(f"\n  📈 Slutthastighet: {df['delta_v'].iloc[-1]:.2f} m/s")
    print(f"     = {df['delta_v'].iloc[-1]*3.6:.1f} km/h")
    
    print(f"\n  📍 Slutthoyde: {df['delta_h'].iloc[-1]:.2f} meter")
    print(f"     ➜ Dronen steg over {df['delta_h'].iloc[-1]:.0f} meter på bare {df['t_s'].max():.1f} sek")
    
    print(f"\n{'='*70}")
    print("⚡ ENERGI OG EFFEKTIVITET:")
    print(f"{'='*70}")
    
    total_energy = (df['Wattage'] * df['dt_s']).sum() / 3600
    energy_per_meter = total_energy / df['delta_h'].iloc[-1] if df['delta_h'].iloc[-1] > 0 else 0
    
    print(f"  Total energiforbruk: {total_energy*1000:.1f} Wh")
    print(f"  Energi per meter: {energy_per_meter*1000:.2f} Wh/m")
    print(f"  ➜ Dronen bruker {energy_per_meter*1000:.2f} Wh for å stige en meter")
    
    print(f"\n{'='*70}")
    print("🔋 BATTERI OG SPENNING:")
    print(f"{'='*70}")
    
    voltage_variation = df['voltage_V'].std()
    print(f"  Gjennomsnittsspenning: {df['voltage_V'].mean():.2f} V")
    print(f"  Spenningsvariasjoner: ±{voltage_variation:.2f} V")
    
    if voltage_variation < 0.5:
        print(f"  ✓ VELDIG STABIL - Batteri er i god form")
    elif voltage_variation < 1:
        print(f"  ⚠ MODERAT STABIL - Normal batteridegradation")
    else:
        print(f"  ⚡ USTABIL - Batteri kan være dårlig")

def normality_test(df):
    """Normalitets-test"""
    print("\n" + "="*70)
    print("NORMALITETS-TEST (Shapiro-Wilk) - ER DATAENE NORMALFORDELT?")
    print("="*70)
    print("\n🔍 FORKLARING:")
    print("Normalfordeling er en bjellekurve - de fleste verdier i midten.")
    print("Mange statistiske tester krever normalfordelte data.")
    print("  • p > 0.05 = Data er NORMALFORDELT ✓")
    print("  • p ≤ 0.05 = Data er IKKE normalfordelt ✗")
    
    cols = ['a_z', 'delta_v']
    for col in cols:
        if col in df.columns and len(df[col]) > 3:
            stat, p_value = stats.shapiro(df[col].dropna()[:len(df[col])//2])
            
            print(f"\n{'='*70}")
            print(f"{col.upper()}:")
            print(f"{'='*70}")
            print(f"  Shapiro-Wilk statistikk: {stat:.4f}")
            print(f"  P-verdi: {p_value:.4f}")
            
            if p_value > 0.05:
                print(f"  ✓ Data er NORMALFORDELT")
                print(f"     Vi kan bruke parametriske tester (t-test, ANOVA)")
            else:
                print(f"  ✗ Data er IKKE normalfordelt")
                print(f"     Vi bør bruke ikke-parametriske tester")

def create_statistical_plots(df):
    """Lag statistiske grafer"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Histogram
    ax = axes[0, 0]
    ax.hist(df['a_z'], bins=20, color='blue', alpha=0.7, edgecolor='black')
    ax.set_xlabel('Akselerasjon [m/s²]')
    ax.set_ylabel('Frekvens')
    ax.set_title('Histogram - Akselerasjon fordeling')
    ax.axvline(df['a_z'].mean(), color='red', linestyle='--', label=f'Mean: {df["a_z"].mean():.2f}')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Q-Q plot
    ax = axes[0, 1]
    stats.probplot(df['a_z'], dist="norm", plot=ax)
    ax.set_title('Q-Q Plot - Normalitetssjekk')
    ax.grid(True, alpha=0.3)
    
    # Box plot
    ax = axes[1, 0]
    box_data = [df['a_z'], df['delta_v'], df['delta_h']]
    ax.boxplot(box_data, labels=['a_z', 'delta_v', 'delta_h'])
    ax.set_ylabel('Verdi')
    ax.set_title('Box Plot - Uteliggere analyse')
    ax.grid(True, alpha=0.3)
    
    # Korrelasjons heatmap
    ax = axes[1, 1]
    cols = ['a_z', 'delta_v', 'delta_h', 'voltage_V', 'Wattage']
    available_cols = [col for col in cols if col in df.columns]
    corr_matrix = df[available_cols].corr()
    im = ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
    ax.set_xticks(range(len(available_cols)))
    ax.set_yticks(range(len(available_cols)))
    ax.set_xticklabels(available_cols, rotation=45, ha='right')
    ax.set_yticklabels(available_cols)
    ax.set_title('Korrelasjons matrix')
    plt.colorbar(im, ax=ax)
    
    fig.tight_layout()
    fig.savefig("out/statistics_plots.png", dpi=150)
    print(f"\n✓ Statistiske grafer lagret: out/statistics_plots.png")

def main():
    print("\n" + "="*60)
    print("STATISTISK ANALYSE AV FPV DRONE DATA")
    print("="*60)
    
    df = load_data()
    if df is None:
        return
    
    # Kjør alle analyser
    descriptive_statistics(df)
    correlation_analysis(df)
    t_test_analysis(df)
    anova_analysis(df)
    normality_test(df)
    qualitative_analysis(df)
    
    # Lag grafer
    create_statistical_plots(df)
    
    print("\n" + "="*60)
    print("✓ ANALYSE FERDIG")
    print("="*60)

if __name__ == "__main__":
    main()

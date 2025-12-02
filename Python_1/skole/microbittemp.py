import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

try:
    from scipy import stats
except ImportError:
    stats = None
import numpy as np

# --- KONFIGURASJON ---
FILNAVN = 'microbit.csv'  # Filnavnet på dataopplastingen fra micro:bit
SMOOTHING_WINDOW = 6  # Hvor mange målinger skal vi glatte over? (6 målinger = 1 time hvis du logger hvert 10. min)
SPLIT_HOURS = 24  # Tidsgrense mellom fase 1 og fase 2 (fredag kl 24:00)
DAY1_FILENAME = 'microbit_day1.csv'
DAY2_FILENAME = 'microbit_day2.csv'

def analyser_data():
    print(f"--- Starter analyse av {FILNAVN} ---")

    # 1. Laste inn data
    # Micro:bit CSV har ofte mellomrom i overskriftene, så vi renser dem litt
    script_folder = Path(__file__).resolve().parent
    fil_sti = script_folder / FILNAVN
    # Hvis dag1/dag2-filer finnes, les dem som to faser, ellers les hovedfilen og del i to
    dag1_sti = script_folder / DAY1_FILENAME
    dag2_sti = script_folder / DAY2_FILENAME
    fase1 = None
    fase2 = None
    if dag1_sti.exists() and dag2_sti.exists():
        try:
            df1 = pd.read_csv(dag1_sti)
            df2 = pd.read_csv(dag2_sti)
            df1.columns = df1.columns.str.strip()
            df2.columns = df2.columns.str.strip()
            # Standardiser kolonnenavn
            tids_kolonne_1 = df1.columns[0]
            temp_kolonne_1 = df1.columns[1]
            tids_kolonne_2 = df2.columns[0]
            temp_kolonne_2 = df2.columns[1]
            df1['Timer'] = df1[tids_kolonne_1] / 3600
            df2['Timer'] = df2[tids_kolonne_2] / 3600
            fase1 = df1
            fase2 = df2
            df = pd.concat([df1, df2], ignore_index=True)
            tids_kolonne = df.columns[0]
            temp_kolonne = df.columns[1]
        except Exception as e:
            print(f"FEIL ved lesing av dag1/dag2-filer: {e}. Forsøker hovedfil.")
    if fase1 is None or fase2 is None:
        try:
            df = pd.read_csv(fil_sti)
            # Fjerner mellomrom i kolonnenavnene (f.eks " time" -> "time")
            df.columns = df.columns.str.strip()
        except FileNotFoundError:
            print(f"FEIL: Finner ikke '{FILNAVN}'. Legg filen i {script_folder} eller oppdater FILNAVN.")
            return

    # 2. Forberede Tids-aksen
    # Micro:bit logger tid i sekunder. Vi vil ha det i timer for helgen.
    # Forutsetter at første kolonne er tid. Sjekk CSV-filen din!
    if fase1 is None or fase2 is None:
        tids_kolonne = df.columns[0] # Første kolonne (tid)
        temp_kolonne = df.columns[1] # Andre kolonne (temp)
        df['Timer'] = df[tids_kolonne] / 3600  # Konverterer sekunder til timer

    # 3. Statistisk Analyse (ToF-krav)
    gjennomsnitt = df[temp_kolonne].mean()
    std_avvik = df[temp_kolonne].std()
    maks_temp = df[temp_kolonne].max()
    min_temp = df[temp_kolonne].min()

    print("\n--- RESULTATER TIL RAPPORTEN ---")
    print(f"Antall målinger: {len(df)}")
    print(f"Gjennomsnittstemperatur: {gjennomsnitt:.2f} °C")
    print(f"Standardavvik: {std_avvik:.2f}")
    print(f"Høyeste temperatur: {maks_temp} °C")
    print(f"Laveste temperatur: {min_temp} °C")
    print("--------------------------------\n")

    # 3.1 Del opp data i faser rundt fredag kl 24:00 (24 timer / 48 timer for helgen)
    if fase1 is None or fase2 is None:
        fase1 = df[df['Timer'] <= SPLIT_HOURS]
        fase2 = df[df['Timer'] > SPLIT_HOURS]

    def skriv_fase_stats(fasenavn, data):
        if data.empty:
            print(f"{fasenavn}: ingen målinger")
            return
        print(f"{fasenavn} ({len(data)} målinger): gjennomsnitt {data.mean():.2f} °C, std {data.std():.2f}")

    print("--- FASEDELING ---")
    skriv_fase_stats('Fase 1 (fredag 00:00-24:00)', fase1[temp_kolonne])
    skriv_fase_stats('Fase 2 (lørdag 00:00-søndag 24:00)', fase2[temp_kolonne])
    print()

    dag1_csv = script_folder / DAY1_FILENAME
    dag2_csv = script_folder / DAY2_FILENAME
    for navn, blokk in ((dag1_csv, fase1), (dag2_csv, fase2)):
        blokk.drop(columns=['Timer'], errors='ignore').to_csv(navn, index=False)
        print(f"{len(blokk)} rader skrevet til {navn.name}")
    print()

    # 3.2 Sammenlikn fasene med grunnleggende statistiske tester
    def kjør_tester(a, b):
        if stats is None:
            print("Installer SciPy for å kjøre t-test og ikke-parametriske tester (pip install scipy).")
            return
        if len(a) < 2 or len(b) < 2:
            print("For få målinger i en av fasene til å kjøre formelle tester.")
            return
        ttest = stats.ttest_ind(a, b, equal_var=False)
        mw = stats.mannwhitneyu(a, b, alternative='two-sided')
        ks = stats.ks_2samp(a, b)
        # 95% konfidensintervall for middelverdi per fase (normal-approx)
        def ci_mean(x):
            n = len(x)
            m = np.mean(x)
            s = np.std(x, ddof=1)
            se = s / np.sqrt(n)
            # bruk t-fordeling
            tcrit = stats.t.ppf(0.975, df=n-1) if stats else 1.96
            return m, m - tcrit*se, m + tcrit*se
        m1, ci1_lo, ci1_hi = ci_mean(a)
        m2, ci2_lo, ci2_hi = ci_mean(b)
        # Cohen's d (pooled SD)
        s1 = np.std(a, ddof=1); s2 = np.std(b, ddof=1)
        n1 = len(a); n2 = len(b)
        sp = np.sqrt(((n1-1)*s1**2 + (n2-1)*s2**2) / (n1+n2-2)) if (n1+n2-2) > 0 else np.nan
        cohens_d = (m2 - m1) / sp if sp and not np.isnan(sp) else np.nan
        print("--- STATISTISKE TESTER ---")
        print(f"Welch t-test: t={ttest.statistic:.2f}, p={ttest.pvalue:.3f}")
        print(f"Mann-Whitney U: U={mw.statistic:.2f}, p={mw.pvalue:.3f}")
        print(f"Kolmogorov-Smirnov: D={ks.statistic:.2f}, p={ks.pvalue:.3f}")
        print(f"Fase 1 95% CI: [{ci1_lo:.2f}, {ci1_hi:.2f}] °C")
        print(f"Fase 2 95% CI: [{ci2_lo:.2f}, {ci2_hi:.2f}] °C")
        print(f"Cohen's d: {cohens_d:.2f}")

    kjør_tester(fase1[temp_kolonne], fase2[temp_kolonne])
    print()

    # 4. "Smoothing" (Glatting av data)
    # Dette fjerner støy og gjør kurven penere.
    # Vi bruker et "Rolling Average".
    df['Glatta_Temp'] = df[temp_kolonne].rolling(window=SMOOTHING_WINDOW).mean()

    # 5. Lage Graf
    plt.figure(figsize=(12, 6)) # Størrelse på bildet

    # Tegn faseinndeling bak linjene
    # Sett riktig område for visning
    x_min = min(fase1['Timer'].min(), fase2['Timer'].min())
    x_max = max(fase1['Timer'].max(), fase2['Timer'].max())
    fase2_end = max(x_max, SPLIT_HOURS + 1)
    plt.axvspan(x_min, min(SPLIT_HOURS, x_max), color='lightskyblue', alpha=0.25, label='Fase 1: fredag 00-24')
    plt.axvspan(max(SPLIT_HOURS, x_min), fase2_end, color='navajowhite', alpha=0.25, label='Fase 2: lørdag 00 - søndag 24')
    plt.axvline(SPLIT_HOURS, color='gray', linestyle='--', linewidth=1)

    # Tegn rådata (litt gjennomsiktig, så vi ser støyen)
    # Tegn rådata fra begge faser for klarhet
    plt.plot(fase1['Timer'], fase1[temp_kolonne], label='Rådata Fase 1', color='dimgray', linewidth=1, alpha=0.7)
    plt.plot(fase2['Timer'], fase2[temp_kolonne], label='Rådata Fase 2', color='darkgray', linewidth=1, alpha=0.7)

    # Tegn glatta data (tydelig linje)
    # Glattede kurver per fase
    if 'Glatta_Temp' in df.columns:
        pass
    fase1['Glatta_Temp'] = fase1[temp_kolonne].rolling(window=SMOOTHING_WINDOW).mean()
    fase2['Glatta_Temp'] = fase2[temp_kolonne].rolling(window=SMOOTHING_WINDOW).mean()
    plt.plot(fase1['Timer'], fase1['Glatta_Temp'], label=f'Trend Fase 1 ({SMOOTHING_WINDOW})', color='red', linewidth=2)
    plt.plot(fase2['Timer'], fase2['Glatta_Temp'], label=f'Trend Fase 2 ({SMOOTHING_WINDOW})', color='orange', linewidth=2)

    # Tegn gjennomsnittslinje
    plt.axhline(y=gjennomsnitt, color='blue', linestyle='--', label=f'Gjennomsnitt ({gjennomsnitt:.1f}°C)')

    # Pynt på grafen
    plt.title('Temperaturutvikling over helgen', fontsize=16)
    plt.xlabel('Tid (Timer)', fontsize=12)
    plt.ylabel('Temperatur (°C)', fontsize=12)
    plt.legend() # Viser hva linjene betyr
    plt.grid(True, alpha=0.3) # Rutenett

    # Lagre grafen som bilde
    plt.savefig('temperatur_graf.png')
    print("Graf er lagret som 'temperatur_graf.png'. Lim denne inn i rapporten!")

    # Enkel lineær regresjon per fase
    def regresjon_info(df_phase):
        x = df_phase['Timer'].to_numpy()
        y = df_phase[temp_kolonne].to_numpy()
        if stats:
            lr = stats.linregress(x, y)
            return lr.slope, lr.intercept, lr.rvalue**2
        else:
            slope, intercept = np.polyfit(x, y, 1)
            y_pred = slope*x + intercept
            ss_res = np.sum((y - y_pred)**2)
            ss_tot = np.sum((y - np.mean(y))**2)
            r2 = 1 - ss_res/ss_tot if ss_tot > 0 else np.nan
            return slope, intercept, r2

    s1, i1, r21 = regresjon_info(fase1)
    s2, i2, r22 = regresjon_info(fase2)
    print("--- REGRESJON (linær) ---")
    print(f"Fase 1: slope={s1:.4f} °C/time, intercept={i1:.2f}, R^2={r21:.3f}")
    print(f"Fase 2: slope={s2:.4f} °C/time, intercept={i2:.2f}, R^2={r22:.3f}")
    
    # Vis grafen på skjermen
    plt.show()

if __name__ == "__main__":
    analyser_data()
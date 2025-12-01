import pandas as pd
import matplotlib.pyplot as plt

# --- KONFIGURASJON ---
FILNAVN = 'data.csv'  # Navnet på filen du lastet ned fra micro:bit
SMOOTHING_WINDOW = 6  # Hvor mange målinger skal vi glatte over? (6 målinger = 1 time hvis du logger hvert 10. min)

def analyser_data():
    print(f"--- Starter analyse av {FILNAVN} ---")

    # 1. Laste inn data
    # Micro:bit CSV har ofte mellomrom i overskriftene, så vi renser dem litt
    try:
        df = pd.read_csv(FILNAVN)
        # Fjerner mellomrom i kolonnenavnene (f.eks " time" -> "time")
        df.columns = df.columns.str.strip()
    except FileNotFoundError:
        print("FEIL: Finner ikke filen. Sjekk at den heter 'data.csv' og ligger i samme mappe.")
        return

    # 2. Forberede Tids-aksen
    # Micro:bit logger tid i sekunder. Vi vil ha det i timer for helgen.
    # Forutsetter at første kolonne er tid. Sjekk CSV-filen din!
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

    # 4. "Smoothing" (Glatting av data)
    # Dette fjerner støy og gjør kurven penere.
    # Vi bruker et "Rolling Average".
    df['Glatta_Temp'] = df[temp_kolonne].rolling(window=SMOOTHING_WINDOW).mean()

    # 5. Lage Graf
    plt.figure(figsize=(12, 6)) # Størrelse på bildet

    # Tegn rådata (litt gjennomsiktig, så vi ser støyen)
    plt.plot(df['Timer'], df[temp_kolonne], 
             label='Rådata (Målinger)', 
             color='lightgray', 
             linewidth=1)

    # Tegn glatta data (tydelig linje)
    plt.plot(df['Timer'], df['Glatta_Temp'], 
             label=f'Trend (Glatta snitt, {SMOOTHING_WINDOW} pkt)', 
             color='red', 
             linewidth=2)

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
    
    # Vis grafen på skjermen
    plt.show()

if __name__ == "__main__":
    analyser_data()
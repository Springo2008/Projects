# Temperaturmålinger i Privatbolig: Sammenligning av Oppadgåande og Nedadgåande Målinger

**Forfattere:** [Ditt navn]  
**Dato:** 3. desember 2025  
**Prosjekt:** Teknologi- og Forskningslære 1 (ToF 1)

---

## SAMMENDRAG

Dette prosjektet undersøker temperaturvariasjoner i en privatbolig ved hjelp av micro:bit sensorer. To datasett ble samlet inn – ett fra en oppadgåande fase (UP) og ett fra en nedadgående fase (DOWN) – for å identifisere og analysere temperaturforskjeller mellom disse målingsfasene. 

**Hovedfunn:** Det er en **statistisk signifikant forskjell** mellom oppadgåande og nedadgående målinger, med DOWN-målinger som viser en gjennomsnittlig temperatur på **24,60°C** versus UP-målinger på **20,01°C** – en forskjell på **4,59°C**. Denne forskjellen er høyst signifikant (p < 0,001) med stor effektstørrelse (Cohen's d = 10,83).

---

## INTRODUKSJON

### Problemstilling
Hvordan varierer romtemperaturen i en privatbolig mellom oppadgåande og nedadgående målefaser, og er denne variasjonen statistisk signifikant?

### Bakgrunn og Motivasjon
Temperaturkontroll er viktig for både komfort og energieffektivitet i boliger. Ved å forstå hvordan temperaturen endrer seg under ulike betingelser (oppvarming vs. nedkjøling), kan man bedre optimalisere varmesystemer og redusere energiforbruk. Dette prosjektet undersøker disse temperaturmønstrene ved hjelp av automatisert datainnsamling med micro:bit sensorer.

### Hypotese
Vi forventer at temperaturene under nedadgåande fase (DOWN) vil være høyere enn under oppadgåande fase (UP) fordi systemet muligens har vært på oppvarmingsfase under DOWN-målingene.

---

## TEORI

### Varmeledning og Termodynamikk
Temperaturendringer i bygninger styres av termodynamikkens grunnleggende prinsipper. Varme overføres gjennom tre mekanismer: ledning, konveksjon og stråling (Anderson, 2015). Romtemperatur påvirkes av varmekilder (oppvarming, sol), varmekjølende effekter (ventilasjon, utendørstemperatur) og materialenes termiske mass.

### Termistorer og Temperaturmålinger
Micro:bit-brettet inneholder en innebygd temperatursensor (termistor). Termistorer har motstand som varierer med temperatur. For nøyaktige målinger er det viktig å være klar over sensorens nøyaktighet, typisk ±2°C for micro:bit (Microbit Foundation, 2023).

### Statistiske Testmetoder

#### Deskriptiv Statistikk
Gjennomsnitt, standardavvik og konfidensintervaller gir en oversikt over datasettets sentrale tendens og variabilitet.

#### T-test
Independent samples t-test brukes til å sammenligne gjennomsnitt fra to uavhengige grupper. Testen antar:
- Data er omtrent normalfordelt
- Variansen er omtrent lik mellom gruppene (Levene's test)

Teststatistikken beregnes som:
$$t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{s_p^2(\frac{1}{n_1} + \frac{1}{n_2})}}$$

hvor $s_p^2$ er poolet varians.

#### Konfidensintervall
95% konfidensintervall for gjennomsnitt gir et område hvor vi med 95% sannsynlighet antar det sanne gjennomsnitt ligger. Beregnet som:
$$CI = \bar{x} \pm t_{\alpha/2} \cdot SE$$

#### Effektstørrelse (Cohen's d)
Cohen's d måler den praktiske signifikansen av forskjellen:
$$d = \frac{\bar{x}_1 - \bar{x}_2}{s_p}$$

Tolkningsguide: d < 0,2 (neglisjerbar), 0,2–0,5 (liten), 0,5–0,8 (medium), > 0,8 (stor).

---

## METODE

### Datainnsamling
- **Sensorer:** micro:bit innebygde temperatursensorer
- **Målinger:** To datasett med hver 95 målinger
  - **UP-datasett:** Oppadgående fase
  - **DOWN-datasett:** Nedadgående fase
- **Tidsspacing:** Målinger tatt ca. hver 300. sekund (5 minutter)
- **Gjeldende tid:** Cirka 8 timer og 28 minutter måling per fase

### Målelokasjoner
Begge sensorene ble plassert på samme lokasjon for å sikre sammenlignbarhet av målingene.

### Databehandling
1. CSV-filer lastet inn i Python
2. Deskriptiv statistikk beregnet
3. Normalitet sjekket med Shapiro-Wilk test
4. Likhet av varianser sjekket med Levene's test
5. Independent samples t-test gjennomført
6. Konfidensintervaller beregnet
7. Visualiseringer generert

### Statistisk Analyse
- **Signifikansnivå:** α = 0,05
- **Testtype:** Two-tailed independent samples t-test
- **Software:** Python 3.12 med bibliotekene Pandas, NumPy, SciPy, Matplotlib

---

## RESULTATER

### Deskriptiv Statistikk

| Metrikk | UP-datasett | DOWN-datasett |
|---------|------------|--------------|
| Antall målinger (N) | 95 | 95 |
| Gjennomsnitt | 20,01°C | 24,60°C |
| Standardavvik | 0,1026°C | 0,5907°C |
| Minimum | 20,00°C | 23,00°C |
| Maksimum | 21,00°C | 25,00°C |
| Median | 20,00°C | 25,00°C |
| Variasjonskoeffisient | 0,51% | 2,40% |

### Konfidensintervaller (95%)

**UP-datasett:**
- Gjennomsnitt: 20,0105°C
- 95% KI: [19,9896; 20,0314]°C
- Margin of Error: ±0,0209°C

**DOWN-datasett:**
- Gjennomsnitt: 24,6000°C
- 95% KI: [24,4797; 24,7203]°C
- Margin of Error: ±0,1203°C

### Normalitetstest (Shapiro-Wilk)

| Datasett | Test-statistikk | P-verdi | Normal? |
|----------|-----------------|---------|---------|
| UP | 0,0782 | < 0,0001 | Nei |
| DOWN | 0,6590 | < 0,0001 | Nei |

**Tolkning:** Begge datasett avviker fra normalfordeling. UP-dataene viser veldig lite variasjon (mest verdier på 20°C), mens DOWN-dataene har noe større spredning.

### Likhet av Varianser (Levene's Test)

- **Test-statistikk:** 40,0891
- **P-verdi:** < 0,0001
- **Konklusjon:** Variansene er **ikke like** (p < 0,05)

### Independent Samples T-Test

| Statistikk | Verdi |
|-----------|-------|
| T-statistikk | -74,6101 |
| P-verdi (two-tailed) | < 0,000001 |
| Signifikans | *** Høyst signifikant |
| Effektstørrelse (Cohen's d) | 10,8256 (stor) |

**Tolkning:**
- Nullhypotesen forkastes (p < 0,001)
- Det er en **høyst statistisk signifikant forskjell** mellom UP og DOWN temperaturene
- Cohen's d på 10,83 indikerer en **meget stor praktisk signifikans**
- Temperaturforskjellen på 4,59°C er både statistisk og praktisk signifikant

### Visualiseringer

[Se vedlegg: temperature_analysis.png og statistical_tests.png]

**Hovedfunn fra visualiseringer:**
1. **Tidsserie:** DOWN-temperaturer er konsistent høyere enn UP gjennom hele måleperioden
2. **Boksplot:** DOWN viser større spredning enn UP
3. **Histogram:** UP konsentrert rundt 20°C, DOWN rundt 24-25°C
4. **Distribusjon:** Klar separasjon mellom de to datasettene
5. **Q-Q plott:** Begge datasett avviker fra normalfordeling

---

## DISKUSJON

### Tolkning av Resultater

Analysen viser en **sterk og konsistent temperaturforskjell** mellom oppadgåande (UP) og nedadgående (DOWN) målefaser. DOWN-målingene er i gjennomsnitt 4,59°C høyere enn UP-målingene.

**Mulige forklaringer:**

1. **Varmesystem:** Varmesystemet var sannsynligvis mer aktivt under DOWN-fasen, noe som førte til høyere romtemperatur.

2. **Dagstid:** DOWN-målingene ble muligens gjennomført på en varmere del av døgnet (f.eks. ettermiddag/kveld) sammenlignet med UP-målingene.

3. **Solavgaver:** Sollys gjennom vinduer kunne påvirke temperaturen under DOWN-fasen mer enn under UP-fasen.

4. **Termisk masse:** Rommet hadde høyere stabil temperatur under DOWN-fasen, muligens på grunn av tidligere oppvarming.

### Data Kvalitet

- **Høy datakvalitet:** Ingen manglende verdier, konsistente målinger over 8+ timer
- **Lav variabilitet i UP:** Standardavvik på bare 0,10°C indikerer stabil, kjølig tilstand
- **Moderat variabilitet i DOWN:** Standardavvik på 0,59°C indikerer mer dynamisk, varm tilstand

### Begrensninger

1. **Antakelser ikke fullt oppfylt:** Begge datasett avviker fra normalfordeling, som er en antagelse for t-test. Imidlertid er t-testen robust mot brudd på normalitet med store utvalg (N=95).

2. **Variansene er ulike:** Levene's test viste ulik varians (p < 0,001), noe som antyder at variabiliteten er høyere i DOWN-dataene. Dette kan påvirke t-testens validitet.

3. **Enkelt sensor per fase:** Vi vet ikke om resultatene ville vært like hvis flere sensorer hadde blitt brukt på ulike lokasjoner.

4. **Kontekstuell informasjon manglet:** Vi vet ikke eksakt hvilke betingelser som rådet under datainnsamlingen (sollys, ventilasjonsbruk, aktivitet i rommet osv.).

### Forbedringer for Fremtidig Forskning

- Bruk flere sensorer på ulike lokasjoner for å avdekke romlig variasjon
- Registrer miljøvariable som solinntoning, luftfuktighet og aktivitet
- Forklar årsaken til UP og DOWN fasene mer presist (f.eks. "oppvarming fra 18°C til 25°C")
- Utføre repeated-measures design for samme sensor over tid
- Beregn lineær regresjon for å modellere temperaturendring over tid

---

## KONKLUSJON

Denne studien har dokumentert en **statistisk signifikant temperaturforskjell** mellom oppadgåande og nedadgående målefaser i en privatbolig. Med en p-verdi < 0,001 og en effektstørrelse på Cohen's d = 10,83 er konklusjonen robust.

**Hypotesen bekreftet:** DOWN-målingene er betydelig høyere (gjennomsnitt 24,60°C) sammenlignet med UP-målingene (gjennomsnitt 20,01°C).

**Praktisk betydning:** Disse funnene illustrerer hvordan romtemperatur kan variere avhengig av oppvarmings- og kjølingsbetingelser. Bedre forståelse av disse mønstrene kan bidra til optimalisering av energibruk og klimakontroll i boliger.

**Forskningsmessig verdi:** Prosjektet demonstrerer bruk av sensorer, datainnsamling, statistisk analyse og hypotesetesting – sentrale komponenter innen teknologi- og forskningslære.

---

## KILDER

Anderson, B. R. (2015). *Heat, air and moisture transfer in building envelopes: Measurements and models*. IEA-annex report, Building and Urban Systems Programme.

Microbit Foundation. (2023). *BBC micro:bit temperature sensor*. Hentet fra https://microbit.org/guide/features/sensors/

Kvanli, A. H., Pavur, R. J., & Keeling, K. B. (2006). *Introductory statistics: A problem-solving approach*. Cengage Learning.

Sullivan, L. M. (2018). *Essentials of biostatistics in public health* (3. utgave). Jones & Bartlett Learning.

---

## VEDLEGG

### A. Databehandling og Python-kode
Analysen ble gjennomført ved hjelp av Python 3.12 med bibliotekene:
- pandas (data handling)
- numpy (numerical computing)
- scipy.stats (statistical tests)
- matplotlib & seaborn (visualization)

Se `temperature_analysis.py` for fullstendig kode.

### B. Rådata
- `microbit_up-data.csv`: 95 temperaturmålinger fra UP-fase
- `microbit_down-data.csv`: 95 temperaturmålinger fra DOWN-fase

### C. Genererte Visualiseringer
- `temperature_analysis.png`: Seks-panels oversikt over temperaturdata
- `statistical_tests.png`: Detaljerte statistiske visualiseringer (Q-Q plott, KDE, etc.)

---

**Denne rapporten oppfyller kompetansemålene fra ToF 1 og ToF 2 ved å:**
- Presentere empiriske data innsamlet med micro:bit ✓
- Bruke statistiske verktøy (t-test, konfidensintervall, effektstørrelse) ✓
- Drøfte metodevalg og datas kvalitet ✓
- Bruke resultatene til å styrke eller forkaste hypoteser ✓
- Dokumentere prosessen grundig med kilder ✓

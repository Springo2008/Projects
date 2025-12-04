# Temperaturanalyse: Rom vs Stue

## Bakgrunn

To micro:bit sensorer ble plassert på ulike lokasjoner i huset for å måle temperaturforskjeller:
- **DOWN-sensor:** Mitt rom (nederste etasje/kjeller)
- **UP-sensor:** 3. etasje, stua

Hver sensor samlet inn 95 temperaturmålinger over en periode på cirka 8,5 timer.

---

## Resultater fra T-test

### Deskriptiv statistikk

| Lokasjon | Gjennomsnitt | Standardavvik | Min | Max |
|----------|-------------|---------------|-----|-----|
| **Mitt rom (DOWN)** | **24,60°C** | 0,59°C | 23°C | 25°C |
| **3. etasje stua (UP)** | **20,01°C** | 0,10°C | 20°C | 21°C |
| **Forskjell** | **+4,59°C** | - | - | - |

### Statistisk test

- **T-statistikk:** -74,61
- **P-verdi:** < 0,001 (p < 0,0001)
- **Konklusjon:** ✓✓✓ **SVÆRT SIGNIFIKANT FORSKJELL**

Denne sterke p-verdien betyr at det er mindre enn 0,01% sannsynlighet for at denne temperaturforskjellen skyldes tilfeldig variasjon.

---

## Tolkning og Forklaring

### Hvorfor er mitt rom varmere?

**1. Varmeopphoping**
Mitt rom ligger nederst i huset, hvor varme fra oppvarming, mennesker, og elektronikk har tendensen til å akkumuleres. Varme stiger naturlig oppover, men i et lukket rom blir varmen fanget.

**2. Mindre luftsirkulasjon**
Et rom som ligger lavere i huset og muligens er mindre ventilert, vil holde på varmen mer effektivt enn en åpen stue på øvre etasjer.

**3. Solinnstråling**
Avhengig av tidspunkt på dagen og årstid, kan direkte eller indirekte solstråling påvirke mitt rom annerledes enn stua. Hvis mitt rom har vinduer som fanger solstråling, kan dette bidra til høyere temperatur.

**4. Aktivitet og varmekilder**
I mitt rom kan det være elektronikk, lamper, eller annen aktivitet som produserer varme. Stua på 3. etasje kan ha mindre varmekilder eller bedre ventilasjon.

### Hvorfor er stua kaldere?

**1. Høyere plassering**
Varme stiger oppover. 3. etasje ligger høyere opp og kan være påvirket av større temperatursvingninger med omgivelsene.

**2. Bedre ventilasjon**
Stuer er ofte større og mer åpne, med bedre luftsirkulasjon som kan føre til mer jevn temperaturfordeling – og potensielt lavere gjennomsnittlig temperatur.

**3. Mindre isolasjon**
Deler av stua på 3. etasje kan være nærmere vegg, tak eller vinduer som er mindre isolert, noe som kan påvirke temperaturen negativt.

**4. Sesongbetingelser**
Hvis målingene ble gjennomført på en kald periode, kan høyere etasjer være påvirket av lavere utetemperatur gjennom vinduer og vegg.

---

## Stabilitet av Temperatur

En interessant observasjon er **stabilitetstmålene**:

- **Mitt rom (DOWN):** Standardavvik = 0,59°C
- **Stua (UP):** Standardavvik = 0,10°C

**Tolkning:**
Stua viser **mye mer stabil** temperatur (mindre variasjon), mens mitt rom har mer **variabilitet**. Dette kan skyldes:
- Stua er større og har mer termisk masse som bufrer temperaturendringer
- Mitt rom er mindre og reagerer raskere på endringer i oppvarming eller aktivitet
- Stua kan ha bedre termisk isolasjon eller balansert klima

---

## Konklusjon

Det er en **klart målbar og statistisk signifikant forskjell** på 4,59°C mellom temperaturen i mitt rom og temperaturen i stua på 3. etasje.

**Mitt rom er varmt** – trolig på grunn av kombinasjonen av:
- Plassering lavt i huset (varme samles nedre)
- Mindre luftsirkulasjon
- Mulige varmekilder
- Mindre termisk stabilitet

**Stua er kjølig** – trolig på grunn av:
- Høyere plassering (varme stiger bort)
- Bedre ventilasjon
- Større termisk masse som stabiliserer temperaturen
- Mulig påvirkning fra utetemperatur

Dette er en klassisk demonstrasjon av hvordan **plassering i huset påvirker romtemperatur**, noe som har praktisk betydning for energisparing og komfort!

---

## Grafisk Framstilling

Se `temperature_plot.png` for visual sammenligning av temperaturkurver over tid. Du kan tydelig se den konsistente separasjonen mellom de to sensorene gjennom hele måleperioden.

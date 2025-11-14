# Gruppeoppgaver torsdag 13. november

Dere skal velge én oppgave per gruppe. Dere har 45 minutter på å gjøre oppgaven sammen. Alle oppgaver skal løses i JavaScript og testes i nettleserens konsoll. Bruk det vi har lært hittil (variabler, operatorer, datatyper, valg, løkker, Math-objektet og modulo). Alle oppgavene krever at dere skriver ut et resultat som gir mening for en som skal teste programmet deres. Det kan også være lurt å teste at programmet fungerer som det skal (console.log() underveis i koden). Etter 45 minutter skal dere presentere løsningen til en annen gruppe. 

Dere skal:
- Beskrive formålet med oppgaven.
- Forklare hvordan dere gikk frem for å planlegge løsningen og fordele oppgaver.
- Forklare koden steg for steg.

## Oppgaver

Velg én av disse oppgavene. Det er ulik vanskelighetsgrad på oppgavene, prøv å utfordre dere selv. Blir dere ferdig med en oppgave, skal dere velge en ny.

### Oppgave 1: Terningturnering (middels)

Lag et program som simulerer en terningturnering mellom tre spillere. Hver spiller skal "trille" en terning 10 ganger og få tilfeldige tall fra 1-6.

Tell hvor mange poeng hver spiller får totalt, og skriv ut hvem som vant til slutt.

### Oppgave 2: Vokal- og bokstavteller (middels)

Be brukeren skrive inn en tekst. 

Programmet skal telle:
- Hvor mange bokstaver teksten totalt har.
- Hvor mange vokaler det er.
- Hvor mange konsonanter det er.

Tips: sjekk ut toLowerCase().

### Oppgave 3: Gjett tallet (middels)

Programmet skal trekke et tilfeldig tall mellom 1 og 50.
Tre spillere får hver sin gjetning (bruk tre prompt()-kall).
Programmet skal skrive ut hvem som kom nærmest tallet.

Tips: Bruk Math.abs() for å finne forskjellen mellom gjetningen og fasiten.

### Oppgave 4: Poengjakt med tilfeldigheter (middels)

Programmet skal kjøre 20 runder. 

Hver runde trekker programmet et tilfeldig tall mellom 1 og 6:
- 1 eller 2 gir +1 poeng.
- 3 eller 4 gir +2 poeng.
- 5 gir +3 poeng.
- 6 gir -2 poeng.

Til slutt skrives totalsummen ut. 

#### Eventuell utvidelse:
Legg til en sjekk: 
- Hvis poengsummen > 25: skriv ut "Du gjorde det bra!".
- Ellers: skriv ut "Prøv igjen!".

### Oppgave 5: Passordgenerator (vanskelig) 

Lag et program som lager et tilfeldig passord med 8 tegn. 

Passordet skal ha:
- Både store og små bokstaver,
- Minst ett tall,
- Minst ett spesialtegn (f.eks. !, #, %).

Programmet skal vise passordet til slutt.

### Oppgave 6: FizzBuzz-spill (vanskelig)

Lag et program som teller fra 1 til 100 og skriver ut:
- "Fizz" - hvis tallet er delelig på 3.
- "Buzz" - hvis tallet er delelig på 5.
- "FizzBuzz" - hvis tallet er delelig på både 3 og 5.

Ellers skrives bare tallet.

### Oppgave 7: Tallspill med bonusrunder (vanskelig)

Lag et program som simulerer et spill der spilleren får 10 runder.
I hver runde trekkes et tilfeldig tall mellom 1 og 20.

- Hvis tallet er oddetall, får spilleren +1 poeng.
- Hvis tallet er partall, får spilleren +2 poeng.
- Hvis tallet er delelig på 5, får spilleren en bonusrunde der et nytt tall trekkes (uten at det teller som en av de 10 runde­ne).
    - Bonusrunden kan gi mellom -3 og +3 poeng.

Etter spillet skal programmet skrive ut:

- Hvor mange poeng spilleren fikk totalt
- Hvor mange bonusrunder som ble spilt
- En liten vurdering basert på poengsummen:
    - Over 20 → “Du er heldig i dag!”
    - Mellom 10 og 20 → “Bra spilt!”
    - Under 10 → “Bedre lykke neste gang!”
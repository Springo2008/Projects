# Paroppgave torsdag 27. november

Velg dere ut minst én oppgave som dere skal gjøre sammen. Dere har 45 minutter på å gjøre oppgaven. Blir dere ferdig med en oppgave, velg en ny. 

Deretter slår vi sammen tre grupper, der hver gruppe skal:

- forklare formålet med oppgaven
- vise hvordan de delte arbeidet
- forklare alle funksjoner og arrays steg for steg
- vise resultatene i konsollen
- la de andre gruppene prøve å løse deres oppgave basert på forklaringen

## Oppgave 1: Klasselistestatistikk (middels)

Lag et program som analyserer en liste med elevnavn. Opprett en array:

```js
let elever = ["Amir", "Sara", "Leo", "Ingrid", "Anna", "Hedda", "Lina", "Oskar"];
```

Sorter navnene alfabetisk ved hjelp av egen sammenligningsfunksjon.

Lag så en funksjon som:

- teller antall elever
- teller hvor mange navn som starter på vokal
- lager en ny array med alle navn som er kortere enn 5 tegn

Skriv ut resultatene på en ryddig måte. 

## Oppgave 2: Terning-spill med historikk (middels)

Simuler et terning-spill hvor spilleren triller en terning 15 ganger. Programmet skal:

- ha en array `kastHistorikk` med alle tallene
- ha en funksjon `trillTerning()` som returnerer et tall 1-6
- ha en funksjon `tellForekomster()` som teller hvor mange ganger hvert tall forekommer (lag én array med 6 verdier)

Skriv ut i konsollen:

- historikken
- antall ganger 1-6 ble trukket
- hvilket tall som kom flest ganger

## Oppgave 3: Filmanbefaler 3000 (middels)

Lag en array med 8 filmer:

```js
let filmer = ["Shrek", "Titanic", "Avatar", "Inception", "Shrek 2", "Cars", "Up", "Dune"];
```

Bruk prompt() til å spørre brukeren om et søkeord. Programmet skal:

- bruke en funksjon som finner alle filmer som inneholder søkeordet
- bruke toLowerCase() slik at søket blir uavhengig av store/små bokstaver
- returnere en ny array med matchende filmer

Hvis listen er tom --> skriv ut "Ingen filmer funnet".

## Oppgave 4: Passordgenerator (vanskelig)

Programmet skal lage 10 passord og lagre dem i en array. Lag en funksjon `lagPassord()` som:

- lager et passord på 8 tegn
- inneholder store bokstaver, små bokstaver, tall og spesialtegn
- bruker `Math.random()`
- returnerer passordet som en streng

Utvidelse: 

- skriv ut alle passord
- skriv ut lengste og korteste passord
- sorter arrayen alfabetisk

## Oppgave 5: Array-transformasjonsmaskin (vanskelig)

Brukeren skriver inn en tekst, f.eks.:

```js
"3, 8, 2, 7, 4, 9, 1"
```

Programmet skal:

- konvertere teksten til en array med tall
- lag funksjoner som 
    - fjerner alle tall
    - dobler alle tall i arrayen
    - sorterer tallene
    - reverserer rekkefølgen uten å bruke `reverse()`
- alle funksjoner skal returnere nye arrayer

Vis array etter hver transformasjon.

## Oppgave 6: Mini-datasett med flerdimensjonale arrayer (vanskelig)

Lag et datasett som en 2D-array, f.eks.: 

```js
let elever = [
  ["Amir", 17, "A"],
  ["Sara", 18, "B"],
  ["Leo", 16, "A"],
  ["Ida", 17, "C"]
];
```

Programmet skal ha funksjoner som:

- finner gjennomsnittsalderen
- returnerer en array med alle elever med karakter A
- finner eldste og yngste elev
- endrer karakteren til en bestemt elev
- sorterer datasettet etter alder
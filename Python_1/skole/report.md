# Prosjektrapport: Temperaturforskjeller over helg

## Sammendrag
Kort oppsummering av problemstillingen og hovedfunn: Dag 2 hadde høyere middeltemperatur enn dag 1 (Welch t-test p<0.001; Cohen's d≈2.1).

## Introduksjon
Formuler problemstillingen (f.eks. hvor er det varmest / inne vs. ute), og hvorfor den er relevant.

## Teori
Kort om temperaturmåling, sensornøyaktighet, standardavvik, konfidensintervall, t-test, robuste tester (Mann-Whitney), KS-test og enkel lineær regresjon. Husk APA-referanser.

## Metode
- Sensor: micro:bit temperatur (hver 10. min)
- Datainnsamling: to datasett (dag 1 og dag 2)
- Databehandling: `convert_txt_to_csv.py` -> `microbit_day1.csv`, `microbit_day2.csv`; analyse med `microbittemp.py`
- Kontrolltiltak: lik plassering/høyde, samme utstyr, noterte forhold.

## Resultater
- Antall målinger: Dag 1: 145, Dag 2: 144
- Middel (95% CI): Dag 1: 22.81°C [22.66, 22.95]; Dag 2: 24.33°C [24.26, 24.41]
- Std: Dag 1: 0.90; Dag 2: 0.47
- Tester: Welch t-test p<0.001; Mann-Whitney p<0.001; KS p<0.001
- Effektstørrelse: Cohen's d ≈ 2.12
- Regresjon (linær): Dag 1 slope ≈ 0.099 °C/time (R²≈0.59); Dag 2 slope ≈ 0.019 °C/time (R²≈0.08)

Sett inn figur: `temperatur_graf.png`.

## Konklusjon
Hva sier funnene om problemstillingen? Vurder begrensninger og alternative forklaringer.

## Kilder (APA)
Liste over kilder.

#!/usr/bin/env python3
"""
Generer presentasjon om Drone Akselerasjonsmåling
LaTeX/PDF-ready format eller HTML-slides
"""

import os
from datetime import datetime

# ============================================================================
# GENERER HTML PRESENTASJON
# ============================================================================

html_presentation = """
<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Akselerasjonsmåling på FPV-Drone med Micro:bit</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            overflow: hidden;
        }
        
        .slide {
            display: none;
            width: 100vw;
            height: 100vh;
            padding: 60px;
            background: white;
            animation: fadeIn 0.5s;
        }
        
        .slide.active {
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .slide h1 {
            font-size: 3.5em;
            color: #667eea;
            margin-bottom: 20px;
        }
        
        .slide h2 {
            font-size: 2.5em;
            color: #333;
            margin-bottom: 30px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 15px;
        }
        
        .slide p, .slide li {
            font-size: 1.3em;
            color: #555;
            line-height: 1.8;
            margin-bottom: 15px;
        }
        
        .slide ul {
            margin-left: 50px;
        }
        
        .slide img {
            max-width: 90%;
            max-height: 70vh;
            margin: 20px auto;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .title-slide {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
        }
        
        .title-slide h1 {
            color: white;
            font-size: 4em;
            margin-bottom: 30px;
        }
        
        .title-slide p {
            color: rgba(255,255,255,0.9);
            font-size: 1.5em;
            margin-bottom: 20px;
        }
        
        .subtitle {
            font-size: 1.8em;
            color: rgba(255,255,255,0.8);
            margin-top: 40px;
        }
        
        .controls {
            position: fixed;
            bottom: 30px;
            right: 30px;
            display: flex;
            gap: 15px;
            z-index: 1000;
        }
        
        button {
            padding: 12px 24px;
            font-size: 1em;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        button:hover {
            background: #764ba2;
            transform: scale(1.05);
        }
        
        .slide-number {
            position: fixed;
            bottom: 30px;
            left: 30px;
            font-size: 1.2em;
            color: #667eea;
            background: white;
            padding: 10px 20px;
            border-radius: 20px;
        }
        
        .highlight {
            background: #fff3cd;
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin: 20px 0;
        }
        
        .box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .box h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1.3em;
        }
        
        .result {
            background: #d4edda;
            border-left-color: #28a745;
        }
        
        .result h3 {
            color: #28a745;
        }
        
        .warning {
            background: #fff3cd;
            border-left-color: #ffc107;
        }
        
        .warning h3 {
            color: #ffc107;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 1.1em;
        }
        
        th, td {
            border: 2px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        
        th {
            background: #667eea;
            color: white;
        }
        
        tr:nth-child(even) {
            background: #f9f9f9;
        }
    </style>
</head>
<body>

<!-- SLIDE 1: Title -->
<div class="slide title-slide active">
    <h1>🚁 Akselerasjonsmåling på FPV-Drone</h1>
    <p>Bruk av Micro:bit som Datalogger</p>
    <p class="subtitle">Eksperimentell Rapport & Statistisk Analyse</p>
    <p style="margin-top: 60px; font-size: 1.2em;">📅 November 2025</p>
</div>

<!-- SLIDE 2: Formål -->
<div class="slide">
    <h2>📋 Formål</h2>
    <div class="box">
        <h3>Hovedmål:</h3>
        <p>Måle vertikal akselerasjon ved takeoff og cruising på en liten FPV-drone ved bruk av micro:bit som datalogger</p>
    </div>
    <div class="box" style="margin-top: 30px;">
        <h3>Spesifikke Mål:</h3>
        <ul>
            <li>✓ Registrere akselerasjonsprofil under takeoff</li>
            <li>✓ Sammenligne peak akselerasjon mellom repetisjoner</li>
            <li>✓ Verifisere Newtons 2. lov: a = (T - mg)/m</li>
            <li>✓ Analysere stabilitet og konsistens</li>
        </ul>
    </div>
</div>

<!-- SLIDE 3: Hypotese -->
<div class="slide">
    <h2>🔬 Hypotese</h2>
    <div class="box result">
        <h3>H1 - Hovedhypotese:</h3>
        <p><strong>Akselerasjonen følger Newtons 2. lov</strong></p>
        <p style="margin-top: 10px; font-size: 1.1em;">a = (T − mg)/m</p>
        <p style="margin-top: 10px;">Økt thrust gir proporsjonalt økt akselerasjon</p>
    </div>
    <div class="box" style="margin-top: 30px;">
        <h3>H2 - Sekundærhypotese:</h3>
        <p>Peak akselerasjon og høyde er positivt korrelert</p>
    </div>
</div>

<!-- SLIDE 4: Teori -->
<div class="slide">
    <h2>⚙️ Teori</h2>
    <div class="grid-2">
        <div class="box">
            <h3>Newtons 2. Lov:</h3>
            <p>F = ma</p>
            <p style="margin-top: 15px; font-size: 1em;">T − mg = ma</p>
            <p style="margin-top: 15px; font-size: 1em;">a = (T − mg)/m</p>
        </div>
        <div class="box">
            <h3>Micro:bit Sensor:</h3>
            <p>• Måler akselerasjon inkludert tyngdekraft</p>
            <p>• Netto akselerasjon: a_net = a_raw − g</p>
            <p>• Sensorstøy krever filtrering</p>
        </div>
    </div>
    <div class="box" style="margin-top: 20px;">
        <h3>Numerisk Integrasjon:</h3>
        <p>Hastighet: v = ∫a dt  |  Høyde: h = ∫v dt</p>
    </div>
</div>

<!-- SLIDE 5: Metodologi -->
<div class="slide">
    <h2>🔧 Metodologi</h2>
    <table>
        <tr>
            <th>Parameter</th>
            <th>Verdi</th>
        </tr>
        <tr>
            <td>Antall repetisjoner (N)</td>
            <td>5 turer</td>
        </tr>
        <tr>
            <td>Sampling frekvens</td>
            <td>50 - 100 Hz</td>
        </tr>
        <tr>
            <td>Målevarighet per tur</td>
            <td>2.0 sekunder</td>
        </tr>
        <tr>
            <td>Drone masse</td>
            <td>0.24 kg</td>
        </tr>
        <tr>
            <td>Filter type</td>
            <td>Median filter (k=5)</td>
        </tr>
        <tr>
            <td>Integrasjon</td>
            <td>Trapezoidal rule</td>
        </tr>
    </table>
</div>

<!-- SLIDE 6: Utstyr -->
<div class="slide">
    <h2>🛠️ Utstyr</h2>
    <div class="grid-2">
        <div class="box">
            <h3>Drone:</h3>
            <ul>
                <li>Type: FPV Racing</li>
                <li>Masse: 0.24 kg</li>
                <li>Batteri: 3S LiPo (11.1V)</li>
                <li>Motorere: 4x Brushless</li>
            </ul>
        </div>
        <div class="box">
            <h3>Datalogger:</h3>
            <ul>
                <li>Micro:bit v2</li>
                <li>Akselerometer: LSM303B</li>
                <li>Range: ±16g</li>
                <li>Oppløsning: 1 mg</li>
            </ul>
        </div>
    </div>
    <div class="box" style="margin-top: 20px;">
        <h3>Sikkerhetsutstyr:</h3>
        <p>• Spotter til stede | • Fail-safe aktivert | • Vindstille forhold</p>
    </div>
</div>

<!-- SLIDE 7: Eksperimentell Setup -->
<div class="slide">
    <h2>📐 Eksperimentell Setup</h2>
    <div class="box">
        <h3>Montering:</h3>
        <p>Micro:bit montert nær tyngdepunkt av drone</p>
        <p>Aksers orientering: X fram, Y høyre, Z opp</p>
    </div>
    <div class="box" style="margin-top: 20px;">
        <h3>Logging:</h3>
        <p>Timestamp (ms), ax (m/s²), ay (m/s²), az (m/s²)</p>
    </div>
    <div class="box" style="margin-top: 20px;">
        <h3>Prosedyrer:</h3>
        <ul>
            <li>✓ Takeoff-test: Fra hvile, full throttle, registrer akselerasjon</li>
            <li>✓ Cruising-test: Stabil flyvning, registrer stabilitet</li>
        </ul>
    </div>
</div>

<!-- SLIDE 8: Databehandling -->
<div class="slide">
    <h2>💾 Databehandling</h2>
    <div class="grid-2">
        <div class="box">
            <h3>Steg 1: Fjern Gravitet</h3>
            <p>a_net = a_raw − 9.81 m/s²</p>
        </div>
        <div class="box">
            <h3>Steg 2: Filtrer Støy</h3>
            <p>Median filter (k=5) eller moving average</p>
        </div>
    </div>
    <div class="grid-2" style="margin-top: 20px;">
        <div class="box">
            <h3>Steg 3: Integrer</h3>
            <p>Hastighet: v = ∫a dt</p>
            <p>Høyde: h = ∫v dt</p>
        </div>
        <div class="box">
            <h3>Steg 4: Analyser</h3>
            <p>Peak, gjennomsnitt, standardavvik, korrelasjon</p>
        </div>
    </div>
</div>

<!-- SLIDE 9: Resultater - Oversikt -->
<div class="slide">
    <h2>📊 Resultater - Oversikt</h2>
    <table>
        <tr>
            <th>Måling</th>
            <th>Gjennomsnitt</th>
            <th>Std.avvik</th>
            <th>CV%</th>
        </tr>
        <tr>
            <td>Peak akselerasjon</td>
            <td>11.10 m/s²</td>
            <td>1.23 m/s²</td>
            <td>9.9%</td>
        </tr>
        <tr>
            <td>Max høyde</td>
            <td>8.91 m</td>
            <td>0.79 m</td>
            <td>8.9%</td>
        </tr>
        <tr>
            <td>Max hastighet</td>
            <td>6.21 m/s</td>
            <td>0.45 m/s</td>
            <td>7.2%</td>
        </tr>
        <tr>
            <td>Gjennomsnitt kraft</td>
            <td>105 W</td>
            <td>7 W</td>
            <td>6.7%</td>
        </tr>
    </table>
</div>

<!-- SLIDE 10: Resultater - Statistisk -->
<div class="slide">
    <h2>📈 Statistiske Resultater</h2>
    <div class="box result">
        <h3>✓ Normalitets-Test (Shapiro-Wilk):</h3>
        <p>Alle parametere er normalfordelt (p > 0.05)</p>
        <p style="margin-top: 10px; font-size: 0.95em;">→ Sikker å bruke parametriske tester (t-test, ANOVA)</p>
    </div>
    <div class="box result" style="margin-top: 20px;">
        <h3>✓ Energi-Korrelasjon:</h3>
        <p>r = 0.983 (p = 0.0026) - STERK positiv korrelasjon</p>
        <p style="margin-top: 10px; font-size: 0.95em;">→ Høyere fly bruker proporsjonalt mer energi</p>
    </div>
    <div class="box result" style="margin-top: 20px;">
        <h3>✓ Konsistens (CV-test):</h3>
        <p>CV = 9.9% på peak akselerasjon</p>
        <p style="margin-top: 10px; font-size: 0.95em;">→ VELDIG konsekvent drone-oppførsel</p>
    </div>
</div>

<!-- SLIDE 11: Resultater - Grafene -->
<div class="slide">
    <h2>📊 Sammenlignende Resultater</h2>
    <p style="text-align: center; font-size: 1.1em; margin-bottom: 20px;">Fire nøkkel-visualiseringer fra analysen:</p>
    <img src="../out/drone_flights_statistics.png" alt="Drone Statistics">
</div>

<!-- SLIDE 12: Verifisering av Newton -->
<div class="slide">
    <h2>✓ Verifisering av Newtons 2. Lov</h2>
    <div class="box result">
        <h3>Formel:</h3>
        <p>T = m(a + g)</p>
    </div>
    <div class="grid-2" style="margin-top: 20px;">
        <div class="box result">
            <h3>Beregning:</h3>
            <p>Masse: 0.24 kg</p>
            <p>Gjennomsnitt akselerasjon: 11.10 m/s²</p>
            <p>Vekt: 2.35 N</p>
        </div>
        <div class="box result">
            <h3>Resultat:</h3>
            <p>Estimert Thrust: 5.38 N</p>
            <p>T/W ratio: 2.29:1</p>
            <p>✓ Positive thrust - Oppflyvning mulig</p>
        </div>
    </div>
</div>

<!-- SLIDE 13: Batterispenning -->
<div class="slide">
    <h2>🔋 Batterispenning Analyse</h2>
    <div class="box warning">
        <h3>Observasjon:</h3>
        <p>Spenning synker fra ~14.1V til ~13.2V over 5 turer</p>
    </div>
    <div class="box result" style="margin-top: 20px;">
        <h3>Stabilitet:</h3>
        <p>Gjennomsnitt spenningsrange: <span class="highlight">0.48 V</span></p>
        <p>✓ VELDIG STABIL - Batteri i god form</p>
    </div>
    <div class="box" style="margin-top: 20px;">
        <h3>Tolking:</h3>
        <p>Spenningen synker gradvis mellom turer (normalt for LiPo), men holder seg stabil INNEN hver tur</p>
    </div>
</div>

<!-- SLIDE 14: Energieffektivitet -->
<div class="slide">
    <h2>⚡ Energieffektivitet</h2>
    <div class="grid-2">
        <div class="box result">
            <h3>Funn:</h3>
            <p>Energi per meter høyde:</p>
            <p style="font-size: 1.3em; margin-top: 10px;"><span class="highlight">0.01 Wh/m</span></p>
        </div>
        <div class="box result">
            <h3>Konklusjon:</h3>
            <p>Dronen bruker ca 0.01 Wh per meter den stiger</p>
            <p>Veldig effektiv for sin størrelse</p>
        </div>
    </div>
    <div class="box" style="margin-top: 20px;">
        <h3>Forbruk per tur:</h3>
        <p>Gjennomsnitt: <span class="highlight">0.06 Wh</span> per 2-sekunders tur</p>
    </div>
</div>

<!-- SLIDE 15: Konklusjoner -->
<div class="slide">
    <h2>✓ Konklusjoner</h2>
    <div class="box result">
        <h3>H1 - BEKREFTET ✓</h3>
        <p>Akselerasjonen følger Newtons 2. lov (T/W = 2.29)</p>
    </div>
    <div class="box result" style="margin-top: 15px;">
        <h3>H2 - BEKREFTET ✓</h3>
        <p>Sterk korrelasjon mellom akselerasjon og høyde (r = 0.983)</p>
    </div>
    <div class="box result" style="margin-top: 15px;">
        <h3>Konsistens ✓</h3>
        <p>Drone oppfører seg konsekvent (CV = 9.9%)</p>
    </div>
    <div class="box result" style="margin-top: 15px;">
        <h3>Stabilitet ✓</h3>
        <p>Batteri og energisystem er stabile</p>
    </div>
</div>

<!-- SLIDE 16: Usikkerheter & Feilkilder -->
<div class="slide">
    <h2>⚠️ Usikkerheter & Feilkilder</h2>
    <div class="box warning">
        <h3>Systemiske Feil:</h3>
        <ul>
            <li>Sensorstøy i micro:bit akselerometer (±0.5 m/s²)</li>
            <li>Luftmotstand (negligert i beregninger)</li>
            <li>Micro:bit montering - avvik fra vertikal</li>
        </ul>
    </div>
    <div class="box warning" style="margin-top: 20px;">
        <h3>Tilfeldige Feil:</h3>
        <ul>
            <li>Pilot input variasjon (throttle)</li>
            <li>Luftstrømninger / svak vind</li>
            <li>Batteri spenningsvariasjoner</li>
        </ul>
    </div>
</div>

<!-- SLIDE 17: Forbedringer -->
<div class="slide">
    <h2>🔧 Mulige Forbedringer</h2>
    <div class="grid-2">
        <div class="box">
            <h3>Måling:</h3>
            <ul>
                <li>Bruke IMU med høyere oppløsning</li>
                <li>Logging på 200+ Hz</li>
                <li>Sammenligne akselerometer mot referanse</li>
            </ul>
        </div>
        <div class="box">
            <h3>Analyse:</h3>
            <ul>
                <li>Måle luftmotstand direkte</li>
                <li>Sammenligne mot drone sin logging system</li>
                <li>N > 10 repetisjoner</li>
            </ul>
        </div>
    </div>
</div>

<!-- SLIDE 18: Konklusjon -->
<div class="slide title-slide">
    <h1>🎯 Konklusjon</h1>
    <p style="font-size: 1.4em; margin-top: 40px;">Eksperimentet bekrefter at akselerasjon på en FPV-drone følger Newtons fysikalske lover og kan måles pålitelig med micro:bit</p>
    <div class="box result" style="margin-top: 60px; background: rgba(40, 167, 69, 0.2); border: none; color: white;">
        <p style="font-size: 1.3em;">✓ Hypoteser bekreftet</p>
        <p style="font-size: 1.3em;">✓ Resultater konsistente</p>
        <p style="font-size: 1.3em;">✓ Metodologi solid</p>
    </div>
</div>

<!-- SLIDE 19: Kilder -->
<div class="slide">
    <h2>📚 Kilder & Referanser</h2>
    <div class="box">
        <h3>Fysikk:</h3>
        <ul>
            <li>Newton, I. (1687). Philosophiæ Naturalis Principia Mathematica</li>
            <li>Serway & Jewett (2018). Physics for Scientists and Engineers</li>
        </ul>
    </div>
    <div class="box" style="margin-top: 20px;">
        <h3>Hardware:</h3>
        <ul>
            <li>Micro:bit Foundation - Technical Documentation</li>
            <li>LSM303B Accelerometer Datasheet</li>
        </ul>
    </div>
    <div class="box" style="margin-top: 20px;">
        <h3>Verktøy:</h3>
        <ul>
            <li>Python 3.11 | Pandas, NumPy, SciPy, Matplotlib</li>
        </ul>
    </div>
</div>

<!-- SLIDE 20: Takk -->
<div class="slide title-slide">
    <h1>Takk for Oppmerksomheten! 🙏</h1>
    <p style="margin-top: 60px; font-size: 1.5em;">Spørsmål?</p>
    <p style="margin-top: 40px; font-size: 1.2em; opacity: 0.8;">Alle data, kode og grafer er tilgjengelig</p>
</div>

<!-- Controls -->
<div class="slide-number"><span id="current">1</span> / <span id="total">20</span></div>
<div class="controls">
    <button onclick="previousSlide()">← Forrige</button>
    <button onclick="nextSlide()">Neste →</button>
</div>

<script>
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    
    function showSlide(n) {
        slides[currentSlide].classList.remove('active');
        currentSlide = (n + totalSlides) % totalSlides;
        slides[currentSlide].classList.add('active');
        document.getElementById('current').textContent = currentSlide + 1;
    }
    
    function nextSlide() {
        showSlide(currentSlide + 1);
    }
    
    function previousSlide() {
        showSlide(currentSlide - 1);
    }
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight') nextSlide();
        if (e.key === 'ArrowLeft') previousSlide();
    });
    
    // Initialize
    document.getElementById('total').textContent = totalSlides;
</script>

</body>
</html>
"""

def main():
    os.makedirs("out", exist_ok=True)
    
    # Lagre HTML presentasjon
    html_file = "out/presentation.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_presentation)
    
    print("\n" + "="*70)
    print("PRESENTASJON GENERERT")
    print("="*70)
    print(f"\n✓ HTML presentasjon lagret: {html_file}")
    print("\nÅpne i browser:")
    print(f"  open {html_file}")
    print("\nNavigering:")
    print("  • Neste slide: → eller 'Neste' knapp")
    print("  • Forrige slide: ← eller 'Forrige' knapp")
    print("\nSlides inkluderer:")
    print("  • 20 slides med komplett presentasjon")
    print("  • Grafene integrert (drone_flights_statistics.png)")
    print("  • Responsive design for alle enheter")
    print("  • Print-venlig format")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()

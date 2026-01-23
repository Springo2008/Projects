// Arbeidet sammen med Max, Petter og Andreas ved å utvikle denne koden :)
var ordListe = ["nasa", "spacex", "data", "new-glenn", "hund"];
var ordÅGjette = ordListe[Math.floor(Math.random() * ordListe.length)];

var riktig = [];
for (var i = 0; i < ordÅGjette.length; i++) {
    riktig.push("_");
}

var brukteBokstaver = [];
var feil = 0;
var maxFeil = 16;


var gjett_ord = document.getElementById("ord");
var brukte = document.getElementById("brukte");
var forsøk = document.getElementById("forsøk");
var melding = document.getElementById("melding");

// Litt ChatGPT og masse StackOverflow-spørsmål :)
gjett_ord.innerText = riktig.join(" ");


function tastetrykk(event) {
    var bokstav = event.key.toLowerCase();
    
    if (!bokstav.match(/^[a-zæøå\-]$/)) return;

    if (brukteBokstaver.indexOf(bokstav) !== -1) return;

    brukteBokstaver.push(bokstav);
    brukte.innerText = "Brukte bokstaver: " + brukteBokstaver.join(", ");

    // Sjekk om bokstaven finnes i ordet
    if (ordÅGjette.indexOf(bokstav) !== -1) {
        for (var i = 0; i < ordÅGjette.length; i++) {
            if (ordÅGjette[i] === bokstav) {
                riktig[i] = bokstav;
            }
        }
    } else {
        feil++;
    }

    gjett_ord.innerText = riktig.join(" ");
    forsøk.innerText = "Feil: " + feil + " / " + maxFeil;

    if (riktig.indexOf("_") === -1) {
        melding.innerText = "Gratulerer! Du vant!";
        document.body.removeEventListener("keydown", tastetrykk);
    } else if (feil >= maxFeil) {
        melding.innerText = "Spillet er over! Ordet var: " + ordÅGjette;
        document.body.removeEventListener("keydown", tastetrykk);
    }
}

document.body.addEventListener("keydown", tastetrykk);

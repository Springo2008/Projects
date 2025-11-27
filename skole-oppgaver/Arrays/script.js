let tall1 = [2,4,6,8];
//fjern 2 og 8
tall1.splice(0, 1);
tall1.splice(2, 1);
console.log(tall1);
//legg til 5 mellom 4 og 6
tall1.splice(1, 0, 5);
tall1.splice(0,0,3);
tall1.splice(4,0,7);

console.log(tall1);
if (tall1[0] === 3) tall1[0] = "tre";
if (tall1[2] === 5) tall1[2] = "fem";
if (tall1[4] === 7) tall1[4] = "syv";

console.log(tall1);

//oppgave 1a
let tall = [7, 11, 13, 17, 19, 23, 43, 47, 53, 59, 61, 67];

//oppgave 1b
console.log(tall)

//oppgave 1c
//lag en list med 20 random tall mellom 1 og 100
let randomTall = [];
randomTall = [45, 23, 78, 12, 89, 34, 67, 91, 56, 28, 73, 15, 82, 41, 64, 19, 95, 38, 52, 71];
console.log(randomTall);

//finn det største tallet
let storste = Math.max(...randomTall);
console.log("Det største tallet er: " + storste);
let minste =Math.min(...randomTall);
console.log("Det minste tallet er: " + minste);


// finn variasjonsbredden av tallene
let variasjonsbredden = storste - minste;
console.log("Variasjonsbredden er: " + variasjonsbredden);
    
// finn gjennomsnittet av tallene
let gjennomsnitt = randomTall.reduce((a, b) => a + b) / randomTall.length;
console.log("Gjennomsnittet er: " + gjennomsnitt);


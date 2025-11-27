let elever = [
  ["Amir", 17, "A"],
  ["Sara", 18, "B"],
  ["Leo", 16, "A"],
  ["Ida", 17, "C"]
];
function gjennomsnittAlder(elever){
    let totalAlder = 0;
    for (let i =0 ; i < elever.length; i++){
        totalAlder += elever[i][1];
    }
    return totalAlder / elever.length;
}

function karakterA(elever){
    let antallA = 0;
    for (let i = 0; i < elever.length; i++){
        if (elever[i][2] === "A"){
            antallA += 1;
        }
    }
    return antallA;
}



console.log("Gjennomsnittalder er:", gjennomsnittAlder(elever));
console.log(karakterA(elever) + " Elever har karakter A");




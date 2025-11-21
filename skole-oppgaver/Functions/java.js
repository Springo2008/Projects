let navn = "AnAn A";
function palindrom(navn){
   let rensNavn = navn.toLowerCase().replace(/ /g, "");

   let reversNavn = rensNavn.split("").reverse().join("");

   if (rensNavn === reversNavn){
       return true;
   } else {
       return false;
   }
}
console.log(palindrom(navn))

let Tall = 29;

function primTall(tall) {

    if (tall <= 1) {
        return false;
    }
    

    for (let i = 2; i < tall; i++) {
        if (tall % i === 0) {
            return false;  
        }
    }
    
    return true;  
}
console.log(primTall(Tall));
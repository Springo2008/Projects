function checkPassword(){
    let riktig = "Sigma123";
    let passord = document.getElementById("passordInput").value;

    while (passord !== riktig){
        passord = prompt("Feil passord! Prøv igjen:");

        // Sjekk om brukeren klikket Avbryt eller skrev ingenting
        if (passord === null){
            document.getElementById("result").innerHTML = "Avbrutt av bruker";
            return;
        }
        
        if (passord === ""){
            document.getElementById("result").innerHTML = "Du må skrive noe!";
            return;
        }
    }
    
    document.getElementById("result").innerHTML = "✅ Riktig passord! Velkommen!";
}
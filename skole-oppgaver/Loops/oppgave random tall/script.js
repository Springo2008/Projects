function generateRandom(){
    let randomNumber = Math.floor(Math.random() * 100000000);
    document.getElementById("result").textContent = randomNumber;
}
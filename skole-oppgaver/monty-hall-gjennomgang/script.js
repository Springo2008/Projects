let bildørEl = document.querySelectorAll("img")

for (let i = 0; i < bildørEl.length; i++){
    bildørEl[i].addEventListener("click", click)
}

let dørbilderID = ["dor1", "dor2", "dor3"]
let vinnerDør = dørbilderID[Math.floor(Math.random()*dørbilderID.length)];
console.log(vinnerDør)

let fase = 1;
let valgDør = null;
let montyDør = null;
let ferdig = false;

function click(e){
    if (ferdig) return;
    let trykkdørEL = e.target;  
    let dørID = trykkdørEL.id;  

    if (fase === 1){
        valgDør = dørID;
        let muligeDører = [];
        for (let i = 0; i < dørbilderID.length; i++){  
            let d = dørbilderID[i]
            if (d != valgDør && d !== vinnerDør){
                muligeDører.push(d);
            }
        }
        
        montyDør = muligeDører[Math.floor(Math.random()*muligeDører.length)];

        let visDørEl = document.querySelector("#" + montyDør) 
        visDørEl.src = "./bilder/geit.png"

        fase = 2;
        return;

    }
    if (dørID === montyDør) return;
    for(let i = 0; i<dørbilderID.length; i++){
        let d = dørbilderID[i]
        let el = document.querySelector("#"+d);
        if (d == vinnerDør) {
            el.src = "./bilder/bil.png"

        }else{
            el.src=  "./bilder/geit.png"
        }
       


    }
}

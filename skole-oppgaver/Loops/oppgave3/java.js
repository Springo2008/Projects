function countWithWhile(){
    let i =1;
    let output ="While"

    while(i<=10){
        output += i + " ";
        i++;
    }
    document.getElementById("result").innerHTML=output;


}

function countWithFor(){
    let output ="For:";

    for (let i=1; i<=10; i++){
        output += i + " ";
    }
    document.getElementById("result").innerHTML=output;
}
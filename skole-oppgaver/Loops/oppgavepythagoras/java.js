let a = "input a";
let b = "input b";
let c = "input c";

function Pythagoras() {
    a = parseFloat(document.getElementById("inputA").value);
    b = parseFloat(document.getElementById("inputB").value);
    c = parseFloat(document.getElementById("inputC").value);
    if (a**2 + b**2 === c**2){
        document.getElementById("result").innerHTML = "Dette er en Pythagoreisk";
        document.getElementById("result").innerHTML += "<br> a: " + a + ", b: " + b + ", c: " + c;
    }else{
        document.getElementById("result").innerHTML = "Dette er ikke en Pythagoreisk";
        document.getElementById("result").innerHTML += "<br> a: " + a + ", b: " + b + ", c: " + c;
    }   

}
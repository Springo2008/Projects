let output ="//spill//"
for (let i = 1; i <= 10000; i++ ){
    if (i % 3 === 0 && i % 5 === 0){ // FizzBuzz hvis tallet er delig med både 3 og 5
        output += "fizzbuzz, ";
    } else if (i % 3 === 0){ // Fizz hvis tallet er delig med 3
        output += "fizz, ";
    } else if (i % 5 === 0){ // Buzz hvis tallet er delig med 5
        output += "buzz, ";
    } else {
        output += i + ", ";
    }
}

document.getElementById("output").innerText = output;

function checkAge() {
    let age = document.getElementById("age").value;
    let result = document.getElementById("result");
    
    if (age < 18){
          result.textContent = "Du får Kjøpe Barnebillet";
    } else if (age >= 18 && age <65) {
        result.textContent ="Du får kjøpe Voksenbillet"
    } else if (age >= 65){
        result.textContent="Du får Kjøpe Honør"
    }
}              

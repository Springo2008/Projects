function checkAge() {
    let age = document.getElementById("age").value;
    let result = document.getElementById("result");
    
    if (age < 18) {
        result.textContent = "Du får ikke kjøpe øl";
    } else {
        result.textContent = "Du får kjøpe øl";
    }
}
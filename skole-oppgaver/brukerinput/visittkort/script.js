const telInput = document.getElementById("tel");
const navnInput = document.getElementById("navn");

function logValues() {
	const tel = telInput.value;
	const navn = navnInput.value;
	console.log({ navn, tel });
}

telInput.addEventListener("input", logValues);
navnInput.addEventListener("input", logValues);
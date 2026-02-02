
function saveText() {
    var textEl = document.getElementById('textArea').value;
    var titleEl = document.getElementById('textTitle').value;
    var downloadLink = document.createElement('a');
    downloadLink.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(textEl));
    downloadLink.download=titleEl+".txt";
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}   
const textarea = document.getElementById("textArea");
textarea.addEventListener("input", function() {
    let total_length = this.value.length;
    let word_count = this.value.trim().split(/\s+/).length;
    document.getElementById("char-length").innerText = total_length +" Letters, "+ word_count +" Words";
})




function disableTxt() {
  var checkbox = document.getElementById("check");
  var text = document.getElementById("textArea");
  var textTitle = document.getElementById("textTitle");
  var element = document.getElementById("p1");

  if (checkbox.checked){
    new Audio('sfx/light-switch-382712.mp3').play()
    text.disabled = true;
    element = document.getElementById('p1').style.backgroundColor = "red";
    textTitle.disabled = true;
    
  } 
  else if (document.getElementById("check").checked = false){
    element = document.getElementById('p1').style.backgroundColor = "rgb(40, 65, 57)";
    textTitle.disabled = false;
    new Audio('sfx/light-switch-382712.mp3').play()

  }
  else{
    text.disabled = false;
    textTitle.disabled = false;
    element = document.getElementById('p1').style.backgroundColor = "rgb(40, 65, 57)";
     new Audio('sfx/light-switch-382712.mp3').play()
  
  
   }
  
}
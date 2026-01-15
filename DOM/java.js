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

  if (checkbox.checked){
    text.disabled = true;
  } else{
    text.disabled = false;
   }
}
  


/*function undisableTxt() {
  
  
}
}

);
*/


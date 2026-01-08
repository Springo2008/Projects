function saveText() {
    var text = document.getElementById('textArea').value;
    var title = document.getElementById('textTitle').value;
    var downloadLink = document.createElement('a');
    downloadLink.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    downloadLink.download=title+".txt";
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink)
}   
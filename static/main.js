
function doTTS(){
    const audoEl = document.querySelector("audio")
    const progressEl = document.querySelector("progress")
    var text = document.querySelector(".text").value
    const language = document.getElementById('source_lang').value;
    audoEl.hidden = true
    progressEl.hidden = false
    fetch('/api/tts', {
      method: 'POST',
      body: JSON.stringify({text, language})
    })
    .then(response => response.blob())
    .then(result => {
        audoEl.src = URL.createObjectURL(result)
        audoEl.hidden = false
        progressEl.hidden = true
    })
    .catch(() => {
         progressEl.hidden = true
    })
}
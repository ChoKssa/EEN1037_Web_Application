function closeFault() {
    document.getElementById("faultStatus").innerText = "Closed";
    alert("Fault marked as closed.");
  }

function addNote(event) {
    event.preventDefault();
    const text = document.getElementById("noteText").value.trim();
    const imageInput = document.getElementById("noteImage");
    if (!text) return;

    const note = document.createElement("li");
    note.className = "note";
    note.innerHTML = text;

    if (imageInput.files.length > 0) {
        const img = document.createElement("img");
        img.src = URL.createObjectURL(imageInput.files[0]);
        note.appendChild(img);
    }

    document.getElementById("noteList").appendChild(note);
    event.target.reset();
}

function saveChanges() {
    const name = document.getElementById("editName").value;
    const status = document.getElementById("editStatus").value;
    const collection = document.getElementById("editCollection").value;
    const techs = document.getElementById("editTechs").value;

    document.getElementById("machineName").innerText = name;
    document.getElementById("machineStatus").innerText = status;
    document.getElementById("machineCollection").innerText = collection;
    document.getElementById("assignedTechs").innerText = techs;

    alert("Machine information updated!");
}

function deleteMachine() {
    if (confirm("Are you sure you want to delete this machine?")) {
    alert("Machine deleted (simulated). Redirecting to machine list.");
    window.location.href = "../machines.html";
    }
}

function addWarning() {
    const input = document.getElementById("warningInput");
    const warningText = input.value.trim();
    if (warningText !== "") {
    const li = document.createElement("li");
    li.textContent = warningText;
    document.getElementById("warningList").appendChild(li);
    input.value = "";
    }
}

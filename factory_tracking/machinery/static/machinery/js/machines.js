console.log("machines = ", machines);
console.log("userRole = ", userRole);
console.log("usernames = ", usernames);

const selectedUsers = new Set();

function loadMachines() {
  const tbody = document.querySelector("#machineTable tbody");
  tbody.innerHTML = "";

  machines.forEach(machine => {
    const tr = document.createElement("tr");
    tr.setAttribute("data-status", machine.status);
    tr.setAttribute("data-collection", machine.collection);
    tr.onclick = () => window.location.href = `/machines/${machine.id}`;

    tr.innerHTML = `
      <td>${machine.name}</td>
      <td>${machine.status}</td>
      <td>${machine.collection}</td>
      <td>${machine.warnings}</td>
      <td>${machine.technicians?.join(", ") || "—"}</td>
      <td>${machine.repairers?.join(", ") || "—"}</td>
    `;

    tbody.appendChild(tr);
  });

  if (userRole === "manager") {
    document.getElementById("managerForm").style.display = "block";
  }
}

function submitMachineForm(event) {
  event.preventDefault();

  const name = document.getElementById("machineName").value;
  const status = document.getElementById("machineStatus").value;
  const collectionInput = document.getElementById("machineCollections").value;
  const collections = collectionInput.split(",").map(x => x.trim()).filter(Boolean);
  const assigned = Array.from(selectedUsers);

  if (name.trim() === "" || status.trim() === "") {
    alert("Please provide a name and status for the machine.");
    return;
  }

  const newMachine = {
    name,
    status,
    collections,
    assigned,
  };

  document.getElementById("hiddenName").value = newMachine.name;
  document.getElementById("hiddenStatus").value = newMachine.status;
  document.getElementById("hiddenCollections").value = newMachine.collections.join(",");
  document.getElementById("hiddenAssigned").value = newMachine.assigned.join(",");

  document.getElementById("machineForm").submit();
}

function applyFilters() {
  const statusFilter = document.getElementById("statusFilter").value.toLowerCase();
  const collectionFilter = document.getElementById("collectionFilter").value.toLowerCase();

  document.querySelectorAll("#machineTable tbody tr").forEach(row => {
    const status = row.getAttribute("data-status").toLowerCase();
    const collection = row.getAttribute("data-collection").toLowerCase();

    const matches = (!statusFilter || status === statusFilter) &&
                    (!collectionFilter || collection.includes(collectionFilter));

    row.style.display = matches ? "" : "none";
  });
}

function setupUserAutocomplete() {
  const input = document.getElementById("userInput");
  const suggestions = document.getElementById("userSuggestions");

  input.addEventListener("input", () => {
    const query = input.value.toLowerCase();
    suggestions.innerHTML = "";

    if (!query) return;

    const matches = usernames.filter(name =>
      name.toLowerCase().includes(query) && !selectedUsers.has(name)
    );

    matches.forEach(name => {
      const li = document.createElement("li");
      li.textContent = name;
      li.onclick = () => {
        selectedUsers.add(name);
        updateSelectedUsers();
        input.value = "";
        suggestions.innerHTML = "";
      };
      suggestions.appendChild(li);
    });
  });

  document.addEventListener("click", (e) => {
    if (!e.target.closest(".autocomplete-input")) {
      suggestions.innerHTML = "";
    }
  });
}

function updateSelectedUsers() {
    const selectedDiv = document.getElementById("selectedUsers");
    selectedDiv.innerHTML = "";

    selectedUsers.forEach(name => {
      const span = document.createElement("span");
      span.textContent = name;
      span.title = "Click to remove";
      span.style.cursor = "pointer";
      span.onclick = () => {
        selectedUsers.delete(name);
        updateSelectedUsers();
      };
      selectedDiv.appendChild(span);
    });
  }

document.getElementById("statusFilter").addEventListener("change", applyFilters);
document.getElementById("collectionFilter").addEventListener("input", applyFilters);

loadMachines();
setupUserAutocomplete();
document.getElementById("machineForm").addEventListener("submit", submitMachineForm);

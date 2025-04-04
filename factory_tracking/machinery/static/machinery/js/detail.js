const selectedEditUsers = new Set(initiallyAssigned || []);

console.log("initiallyAssigned", initiallyAssigned);


function updateEditAssignedUsers() {
    const container = document.getElementById("editSelectedUsers");
    if (!container) return;

    container.innerHTML = "";

    selectedEditUsers.forEach(username => {
      const wrapper = document.createElement("span");
      wrapper.className = "user-pill";
      wrapper.title = "Click to remove";
      wrapper.innerHTML = `${username} <span class="remove">&times;</span>`;
      wrapper.onclick = () => {
        selectedEditUsers.delete(username);
        updateEditAssignedUsers();
      };
      container.appendChild(wrapper);
    });

    const hiddenInput = document.getElementById("editAssignedHidden");
    if (hiddenInput) {
      hiddenInput.value = Array.from(selectedEditUsers).join(",");
    }
  }


function setupEditUserAutocomplete() {
  const input = document.getElementById("editUserInput");
  const suggestions = document.getElementById("editUserSuggestions");

  input.addEventListener("input", () => {
    const query = input.value.toLowerCase();
    suggestions.innerHTML = "";

    if (!query) return;

    const matches = allUsernames.filter(name =>
      name.toLowerCase().includes(query) && !selectedEditUsers.has(name)
    );

    matches.forEach(name => {
      const li = document.createElement("li");
      li.textContent = name;
      li.onclick = () => {
        selectedEditUsers.add(name);
        updateEditAssignedUsers();
        input.value = "";
        suggestions.innerHTML = "";
      };
      suggestions.appendChild(li);
    });
  });

  document.addEventListener("click", e => {
    if (!e.target.closest(".autocomplete-input")) {
      suggestions.innerHTML = "";
    }
  });
}

document.getElementById("editMachineForm").addEventListener("submit", function (e) {
    const hiddenInput = document.getElementById("editAssignedHidden");
    if (hiddenInput) {
      hiddenInput.value = Array.from(selectedEditUsers).join(",");
    }
  });

document.getElementById("deleteMachineForm")?.addEventListener("submit", function (e) {
    const confirmDelete = confirm("Are you sure you want to delete this machine? This action is irreversible.");
    if (!confirmDelete) {
        e.preventDefault();
    }
});


updateEditAssignedUsers();
setupEditUserAutocomplete();

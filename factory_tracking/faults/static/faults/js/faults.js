function setupMachineAutocomplete() {
    const input = document.getElementById("machineInput");
    const suggestions = document.getElementById("machineSuggestions");
    const hidden = document.getElementById("machineHidden");

    input.addEventListener("input", () => {
        const query = input.value.toLowerCase();
        suggestions.innerHTML = "";

        if (!query) return;

        const matches = machineNames.filter(name =>
        name.toLowerCase().includes(query)
        );

        matches.forEach(name => {
        const li = document.createElement("li");
        li.textContent = name;
        li.onclick = () => {
            input.value = name;
            hidden.value = name;
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

setupMachineAutocomplete();

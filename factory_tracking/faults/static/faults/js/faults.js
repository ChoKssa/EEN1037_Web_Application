const faultList = [
    { id: 1, machine: "Welder X100", desc: "Smoke detected near sensor", status: "Open" },
    { id: 2, machine: "PaintBot 3000", desc: "Paint sprayer jammed", status: "Open" }
];

function loadFaults() {
const tbody = document.getElementById("faultTable");
tbody.innerHTML = "";
faultList.forEach(fault => {
    const tr = document.createElement("tr");
    tr.onclick = () => window.location.href = `/faults/${fault.id}`;
    tr.innerHTML = `
    <td>${fault.id}</td>
    <td>${fault.machine}</td>
    <td>${fault.desc}</td>
    <td>${fault.status}</td>
    `;
    tbody.appendChild(tr);
});
}

function submitFault(e) {
    e.preventDefault();
    const machine = document.getElementById("faultMachine").value;
    const desc = document.getElementById("faultDescription").value;
    const id = faultList.length + 1;
    faultList.push({ id, machine, desc, status: "Open" });
    alert("Fault reported successfully.");
    e.target.reset();
    loadFaults();
}

loadFaults();

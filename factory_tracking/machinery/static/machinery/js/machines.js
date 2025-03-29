const machines = [
    {
        id: 1,
        name: "Welder X100",
        status: "OK",
        collection: "Line A",
        warnings: 0,
        technicians: ["John", "Priya"],
        assignedTo: ["technician"]
    },
    {
        id: 2,
        name: "PaintBot 3000",
        status: "Warning",
        collection: "Line B",
        warnings: 2,
        technicians: ["Alex"],
        assignedTo: ["technician", "repairer"]
    },
    {
        id: 3,
        name: "Conveyor Z",
        status: "Fault",
        collection: "Line A",
        warnings: 5,
        technicians: [],
        assignedTo: ["repairer"]
    }
];

const userRole = "manager"; //  manager Change to "technician" or "repairer" for testing

function loadMachines() {
const tbody = document.querySelector("#machineTable tbody");
tbody.innerHTML = "";

machines.forEach(machine => {
    const isAssigned = machine.assignedTo?.includes(userRole);
    if (userRole === "manager" || isAssigned) {
    const tr = document.createElement("tr");
    tr.setAttribute("data-status", machine.status);
    tr.setAttribute("data-collection", machine.collection);
    tr.onclick = () => window.location.href = `/machines/${machine.id}`;

    tr.innerHTML = `
        <td>${machine.name}</td>
        <td>${machine.status}</td>
        <td>${machine.collection}</td>
        <td>${machine.warnings}</td>
        <td>${machine.technicians.join(", ")}</td>
        <td>
        ${userRole === "manager" ? `<button onclick="event.stopPropagation(); alert('Edit ${machine.name}')">Edit</button>` : ""}
        ${userRole === "technician" ? `<button onclick="event.stopPropagation(); alert('Add Warning')">+ Warning</button>` : ""}
        ${(userRole === "technician" || userRole === "repairer") ? `<button onclick="event.stopPropagation(); alert('Remove Warning')">- Warning</button>` : ""}
        </td>
    `;
    tbody.appendChild(tr);
    }
});

if (userRole === "manager") {
    document.getElementById("managerForm").style.display = "block";
}
}

function submitMachineForm(event) {
event.preventDefault();
const name = document.getElementById("machineName").value;
const status = document.getElementById("machineStatus").value;
const collection = document.getElementById("machineCollection").value;
const assigned = document.getElementById("assignedRoles").value.split(",").map(x => x.trim());
const techs = document.getElementById("technicians").value.split(",").map(x => x.trim());

const newMachine = {
    id: machines.length + 1,
    name: name,
    status: status,
    collection: collection,
    warnings: 0,
    technicians: techs,
    assignedTo: assigned
};

machines.push(newMachine);
loadMachines();
alert("Machine added!");
event.target.reset();
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

document.getElementById("statusFilter").addEventListener("change", applyFilters);
document.getElementById("collectionFilter").addEventListener("input", applyFilters);

loadMachines();

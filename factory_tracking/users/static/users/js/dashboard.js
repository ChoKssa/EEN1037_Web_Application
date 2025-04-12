window.toggleTotal = function () {
  const t = document.getElementById("stat-details-total");
  console.log("Toggling total");
  t.classList.toggle("hidden");
};

window.toggleOK = function () {
  const t = document.getElementById("stat-details-ok");
  console.log("Toggling OK");
  t.classList.toggle("hidden");
};

window.toggleFault = function () {
  const t = document.getElementById("stat-details-fault");
  console.log("Toggling Fault");
  t.classList.toggle("hidden");
};

window.toggleWarning = function () {
  const t = document.getElementById("stat-details-warning");
  console.log("Toggling Warning");
  t.classList.toggle("hidden");
};
const statusCanvas = document.getElementById("statusPieChart");
if (statusCanvas) {
  const ctxStatus = statusCanvas.getContext("2d");

  new Chart(ctxStatus, {
    type: "pie",
    data: {
      labels: Labels,
      datasets: [
        {
          data: Counts,
          backgroundColor: ["#2e7d32", "#c62828", "#f57c00"],
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom",
        },
      },
    },
  });
}


function editUser(id, email, username, role) {
  const formTitle = document.getElementById("formTitle");
  const formWrapper = document.getElementById("userFormWrapper");

  document.getElementById("userId").value = id;
  document.getElementById("email").value = email;
  document.getElementById("username").value = username;
  document.getElementById("role").value = role;

  document.getElementById("passwordLabel").style.display = "none";
  document.getElementById("password").required = false;

  formTitle.innerText = "Edit User";
  formWrapper.classList.remove("hidden");
}

function toggleUserForm(edit = false) {
  const formWrapper = document.getElementById("userFormWrapper");
  const formTitle = document.getElementById("formTitle");

  if (!edit) {
    document.getElementById("userForm").reset();
    document.getElementById("userId").value = "";

    document.getElementById("passwordLabel").style.display = "block";
    document.getElementById("password").required = true;

    formTitle.innerText = "Create User";
  }

  formWrapper.classList.toggle("hidden");
}

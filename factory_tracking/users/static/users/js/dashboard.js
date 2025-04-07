document.addEventListener("DOMContentLoaded", () => {
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
  
  

 
});

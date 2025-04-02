import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export async function renderAdherenceReportsV1() {
  const mainContent = document.getElementById("main-content");
  mainContent.innerHTML = '<div class="loader">Loading adherence data...</div>';

  try {
    const adherenceData = await fetchAdherenceData();
    const medicationData = await fetchMedicationData();

    const adherenceReportHTML = `
            <h1>Medication Adherence Report</h1>
            <div class="adherence-overview">
                <div class="card overall-adherence">
                    <h2>Overall Adherence</h2>
                    <div class="adherence-percentage" id="overall-adherence"></div>
                </div>
                <div class="card adherence-trend">
                    <h2>Monthly Adherence Trend</h2>
                    <canvas id="adherence-trend-chart"></canvas>
                </div>
            </div>
            <div class="card medication-breakdown">
                <h2>Medication Adherence Breakdown</h2>
                <table class="adherence-table">
                    <thead>
                        <tr>
                            <th>Medication</th>
                            <th>Adherence Rate</th>
                            <th>Missed Doses</th>
                            <th>Total Doses</th>
                        </tr>
                    </thead>
                    <tbody id="medication-adherence-body"></tbody>
                </table>
            </div>
            <div class="card daily-adherence">
                <h2>Daily Adherence Heatmap</h2>
                <div id="adherence-heatmap"></div>
            </div>
        `;

    mainContent.innerHTML = adherenceReportHTML;

    renderOverallAdherence(adherenceData);
    renderAdherenceTrendChart(adherenceData);
    renderMedicationBreakdown(adherenceData, medicationData);
    renderAdherenceHeatmap(adherenceData);
  } catch (error) {
    console.error("Error fetching adherence data:", error);
    mainContent.innerHTML =
      "<p>Error loading adherence data. Please try again later.</p>";
  }
}

async function fetchAdherenceData() {
  const response = await fetch("/api/adherence");
  if (!response.ok) {
    throw new Error("Failed to fetch adherence data");
  }
  return response.json();
}

async function fetchMedicationData() {
  const response = await fetch("/api/medications");
  if (!response.ok) {
    throw new Error("Failed to fetch medication data");
  }
  return response.json();
}

function renderOverallAdherence(adherenceData) {
  const overallAdherence = calculateOverallAdherence(adherenceData);
  const adherenceElement = document.getElementById("overall-adherence");
  adherenceElement.textContent = `${overallAdherence}%`;
  adherenceElement.style.color = getAdherenceColor(overallAdherence);
}

function calculateOverallAdherence(adherenceData) {
  const totalDoses = adherenceData.reduce(
    (sum, day) => sum + day.totalDoses,
    0,
  );
  const takenDoses = adherenceData.reduce(
    (sum, day) => sum + day.takenDoses,
    0,
  );
  return Math.round((takenDoses / totalDoses) * 100);
}

function renderAdherenceTrendChart(adherenceData) {
  const ctx = document.getElementById("adherence-trend-chart").getContext("2d");
  new Chart(ctx, {
    type: "line",
    data: {
      labels: adherenceData.map((day) => day.date),
      datasets: [
        {
          label: "Adherence Rate",
          data: adherenceData.map(
            (day) => (day.takenDoses / day.totalDoses) * 100,
          ),
          borderColor: "rgb(75, 192, 192)",
          tension: 0.1,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          title: {
            display: true,
            text: "Adherence Rate (%)",
          },
        },
        x: {
          title: {
            display: true,
            text: "Date",
          },
        },
      },
    },
  });
}

function renderMedicationBreakdown(adherenceData, medicationData) {
  const medicationAdherence = calculateMedicationAdherence(
    adherenceData,
    medicationData,
  );
  const tableBody = document.getElementById("medication-adherence-body");

  medicationAdherence.forEach((med) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td>${med.name}</td>
            <td>${med.adherenceRate}%</td>
            <td>${med.missedDoses}</td>
            <td>${med.totalDoses}</td>
        `;
    tableBody.appendChild(row);
  });
}

function calculateMedicationAdherence(adherenceData, medicationData) {
  const medicationAdherence = medicationData.map((med) => ({
    id: med.id,
    name: med.brand_name,
    takenDoses: 0,
    totalDoses: 0,
  }));

  adherenceData.forEach((day) => {
    day.medications.forEach((medDose) => {
      const medAdherence = medicationAdherence.find(
        (m) => m.id === medDose.medicationId,
      );
      if (medAdherence) {
        medAdherence.takenDoses += medDose.taken ? 1 : 0;
        medAdherence.totalDoses += 1;
      }
    });
  });

  return medicationAdherence.map((med) => ({
    ...med,
    adherenceRate: Math.round((med.takenDoses / med.totalDoses) * 100),
    missedDoses: med.totalDoses - med.takenDoses,
  }));
}

function renderAdherenceHeatmap(adherenceData) {
  const heatmapContainer = document.getElementById("adherence-heatmap");
  const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  const heatmapHTML = `
        <div class="heatmap-grid">
            ${daysOfWeek.map((day) => `<div class="heatmap-label">${day}</div>`).join("")}
            ${adherenceData
              .map((day) => {
                const adherenceRate = (day.takenDoses / day.totalDoses) * 100;
                return `<div class="heatmap-cell" style="background-color: ${getAdherenceColor(adherenceRate)};" title="${day.date}: ${Math.round(adherenceRate)}% adherence"></div>`;
              })
              .join("")}
        </div>
    `;

  heatmapContainer.innerHTML = heatmapHTML;
}

function getAdherenceColor(adherenceRate) {
  if (adherenceRate >= 90) return "#4CAF50";
  if (adherenceRate >= 80) return "#8BC34A";
  if (adherenceRate >= 70) return "#CDDC39";
  if (adherenceRate >= 60) return "#FFEB3B";
  if (adherenceRate >= 50) return "#FFC107";
  return "#FF5722";
}

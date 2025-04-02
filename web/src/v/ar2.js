import { Chart, registerables } from "chart.js";
Chart.register(...registerables);

export async function renderAdherenceReportsV2() {
  const mainContent = document.getElementById("main-content");
  mainContent.innerHTML = '<div class="loader">Loading adherence data...</div>';

  try {
    const adherenceData = await fetchAdherenceData();
    const medicationData = await fetchMedicationData();

    const adherenceReportHTML = `
            <h1>Weekly Medication Adherence Report</h1>
            <div class="week-selector">
                <button id="prev-week">&lt; Previous Week</button>
                <span id="current-week"></span>
                <button id="next-week">Next Week &gt;</button>
            </div>
            <div class="adherence-grid">
                <div class="card weekly-overview">
                    <h2>Weekly Overview</h2>
                    <canvas id="weekly-adherence-chart"></canvas>
                </div>
                <div class="card daily-breakdown">
                    <h2>Daily Breakdown</h2>
                    <div id="daily-adherence-list"></div>
                </div>
                <div class="card medication-performance">
                    <h2>Medication Performance</h2>
                    <canvas id="medication-performance-chart"></canvas>
                </div>
                <div class="card adherence-stats">
                    <h2>Adherence Statistics</h2>
                    <div id="adherence-stats-content"></div>
                </div>
            </div>
        `;

    mainContent.innerHTML = adherenceReportHTML;

    const currentDate = new Date();
    let currentWeekStart = getWeekStart(currentDate);

    renderWeeklyAdherence(adherenceData, medicationData, currentWeekStart);

    document.getElementById("prev-week").addEventListener("click", () => {
      currentWeekStart.setDate(currentWeekStart.getDate() - 7);
      renderWeeklyAdherence(adherenceData, medicationData, currentWeekStart);
    });

    document.getElementById("next-week").addEventListener("click", () => {
      currentWeekStart.setDate(currentWeekStart.getDate() + 7);
      renderWeeklyAdherence(adherenceData, medicationData, currentWeekStart);
    });
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

function getWeekStart(date) {
  const d = new Date(date);
  const day = d.getDay();
  const diff = d.getDate() - day + (day === 0 ? -6 : 1);
  return new Date(d.setDate(diff));
}

function renderWeeklyAdherence(adherenceData, medicationData, weekStart) {
  const weekEnd = new Date(weekStart);
  weekEnd.setDate(weekEnd.getDate() + 6);

  document.getElementById("current-week").textContent =
    `${weekStart.toDateString()} - ${weekEnd.toDateString()}`;

  const weekData = adherenceData.filter((day) => {
    const date = new Date(day.date);
    return date >= weekStart && date <= weekEnd;
  });

  renderWeeklyAdherenceChart(weekData);
  renderDailyBreakdown(weekData, medicationData);
  renderMedicationPerformance(weekData, medicationData);
  renderAdherenceStats(weekData);
}

function renderWeeklyAdherenceChart(weekData) {
  const ctx = document
    .getElementById("weekly-adherence-chart")
    .getContext("2d");
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      datasets: [
        {
          label: "Adherence Rate",
          data: weekData.map((day) => (day.takenDoses / day.totalDoses) * 100),
          backgroundColor: "rgba(75, 192, 192, 0.6)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
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
      },
    },
  });
}

function renderDailyBreakdown(weekData, medicationData) {
  const dailyAdherenceList = document.getElementById("daily-adherence-list");
  dailyAdherenceList.innerHTML = "";

  weekData.forEach((day) => {
    const dayElement = document.createElement("div");
    dayElement.className = "daily-adherence-item";
    const adherenceRate = (day.takenDoses / day.totalDoses) * 100;
    dayElement.innerHTML = `
            <h3>${new Date(day.date).toLocaleDateString("en-US", { weekday: "long" })}</h3>
            <p>Adherence: ${Math.round(adherenceRate)}%</p>
            <ul>
                ${day.medications
                  .map((med) => {
                    const medication = medicationData.find(
                      (m) => m.id === med.medicationId,
                    );
                    return `<li>${medication.brand_name}: ${med.taken ? "Taken" : "Missed"}</li>`;
                  })
                  .join("")}
            </ul>
        `;
    dailyAdherenceList.appendChild(dayElement);
  });
}

function renderMedicationPerformance(weekData, medication) {
  const medicationPerformance = calculateMedicationPerformance(
    weekData,
    medication,
  );

  const ctx = document
    .getElementById("medication-performance-chart")
    .getContext("2d");
  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: medicationPerformance.map((med) => med.name),
      datasets: [
        {
          data: medicationPerformance.map((med) => med.adherenceRate),
          backgroundColor: [
            "#FF6384",
            "#36A2EB",
            "#FFCE56",
            "#4BC0C0",
            "#9966FF",
            "#FF9F40",
          ],
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "right",
        },
      },
    },
  });
}

function calculateMedicationPerformance(weekData, medicationData) {
  const medicationPerformance = medicationData.map((med) => ({
    id: med.id,
    name: med.brand_name,
    takenDoses: 0,
    totalDoses: 0,
  }));

  weekData.forEach((day) => {
    day.medications.forEach((medDose) => {
      const medPerformance = medicationPerformance.find(
        (m) => m.id === medDose.medicationId,
      );
      if (medPerformance) {
        medPerformance.takenDoses += medDose.taken ? 1 : 0;
        medPerformance.totalDoses += 1;
      }
    });
  });

  return medicationPerformance.map((med) => ({
    ...med,
    adherenceRate: Math.round((med.takenDoses / med.totalDoses) * 100),
  }));
}

function renderAdherenceStats(weekData) {
  const statsContent = document.getElementById("adherence-stats-content");
  const totalDoses = weekData.reduce((sum, day) => sum + day.totalDoses, 0);
  const takenDoses = weekData.reduce((sum, day) => sum + day.takenDoses, 0);
  const missedDoses = totalDoses - takenDoses;
  const adherenceRate = (takenDoses / totalDoses) * 100;

  statsContent.innerHTML = `
        <p><strong>Total Doses:</strong> ${totalDoses}</p>
        <p><strong>Taken Doses:</strong> ${takenDoses}</p>
        <p><strong>Missed Doses:</strong> ${missedDoses}</p>
        <p><strong>Adherence Rate:</strong> ${Math.round(adherenceRate)}%</p>
    `;
}

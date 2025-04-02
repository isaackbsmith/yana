export async function renderDashboard() {
  const mainContent = document.getElementById("main-content");
  mainContent.innerHTML = '<div class="loader">Loading dashboard data...</div>';

  try {
    const [userData, medicationData, adherenceData] = await Promise.all([
      fetch("/api/user").then((res) => res.json()),
      fetch("/api/medications").then((res) => res.json()),
      fetch("/api/adherence").then((res) => res.json()),
    ]);

    const dashboardHTML = `
            <h1>Dashboard</h1>
            <div class="dashboard-grid">
                <div class="card personal-details">
                    <h2>Personal Details</h2>
                    <dl>
                        <dt>Name</dt>
                        <dd>${userData.name}</dd>
                        <dt>Blood Type</dt>
                        <dd>${userData.bloodType}</dd>
                        <dt>Height</dt>
                        <dd>${userData.height}</dd>
                        <dt>Weight</dt>
                        <dd>${userData.weight}</dd>
                    </dl>
                </div>
                <div class="card adherence-chart">
                    <h2>Medication Adherence</h2>
                    <canvas id="adherenceChart"></canvas>
                </div>
            </div>
            <div class="card">
                <h2>Recent Medications</h2>
                <table class="medication-list">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Dosage</th>
                            <th>Frequency</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${medicationData
                          .map(
                            (med) => `
                            <tr>
                                <td>${med.name}</td>
                                <td>${med.dosage}</td>
                                <td>${med.frequency}</td>
                                <td><span class="status status-${med.status}">${med.status}</span></td>
                            </tr>
                        `,
                          )
                          .join("")}
                    </tbody>
                </table>
            </div>
        `;

    mainContent.innerHTML = dashboardHTML;

    // Create adherence chart
    const ctx = document.getElementById("adherenceChart").getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: adherenceData.map((d) => d.date),
        datasets: [
          {
            label: "Adherence Rate",
            data: adherenceData.map((d) => d.adherenceRate),
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
          },
        },
      },
    });
  } catch (error) {
    console.error("Error fetching dashboard data:", error);
    mainContent.innerHTML =
      "<p>Error loading dashboard data. Please try again later.</p>";
  }
}

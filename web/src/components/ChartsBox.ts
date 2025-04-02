import { qs } from "../selectors";
import { ComponentProps } from "../types";
import { datetimeFormatter, fetchAdherenceData, insertElement } from "../utils";
import { Chart, ChartConfiguration, ChartData, ChartOptions } from "chart.js/auto";


export default async (props: ComponentProps): Promise<Element | undefined> => {
  const chartsHTML = `
      <h2> Adherence Tracking </h2>
      <div class="adherence-container">
        <div id="adherence-chart">
          <canvas id="chart-2"></canvas>
        </div>
        <div id="adherence-chart">
          <canvas id="chart-1"></canvas>
        </div>
      </div>
    `
  try {
    insertElement({ parent: props.parent, child: chartsHTML, position: "beforeend" })

    const ctx1 = qs<HTMLCanvasElement>("#chart-1")!.getContext("2d")!;
    const ctx2 = qs<HTMLCanvasElement>("#chart-2")!.getContext("2d")!;
    const data = await fetchAdherenceData();
    console.log(data);
    const labels1 = data.map(entry => datetimeFormatter.format(new Date(entry.datetime)));
    const adherenceValues = data.map(entry => entry.adherence_status === 'fully_adherent' ? 1 : entry.adherence_status === null ? -1 : 0);  // 1 for taken, 0 for missed

    // Count the number of different adherence statuses
    const statusCounts = data.reduce((counts: { [key: string]: number }, status) => {
      counts[status.adherence_status || "not_adherent"] = (counts[status.adherence_status || 'not_adherent'] || 0) + 1;
      return counts;
    }, {});

    // Prepare the data for the polar area chart
    const labels2 = Object.keys(statusCounts);
    const adherenceValues2 = Object.values(statusCounts);


    const myChart = new Chart(ctx1, {
      type: "polarArea",
      data: {
        labels: labels2,
        datasets: [{
          data: adherenceValues2,
          backgroundColor: [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'
          ]
        }]
      },
      options: {
        responsive: true,
      },
    });

    const chartData: ChartData = {
      labels: labels1,
      datasets: [{
        label: 'Adherence',
        data: adherenceValues,
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderWidth: 2,
        pointBackgroundColor: data.map(item =>
          item.adherence_status === 'fully_adherent' ? 'rgba(75, 192, 192, 1)' : item.adherence_status === null ? 'rgba(0, 0, 255, 1)' : 'rgba(255, 99, 132, 1)'
        ),
        pointBorderColor: '#fff',
        pointRadius: 6,
        pointHoverRadius: 8,
        fill: true,
        tension: 0.1
      }]
    };

    const options: ChartOptions = {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: false,
        },
        title: {
          display: true,
          text: 'Medication Adherence Over Time',
          font: {
            size: 18,
            weight: 'bold'
          },
          padding: {
            top: 10,
            bottom: 30
          }
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              return context.parsed.y === 1 ? 'Taken' : context.parsed.y === -1 ? 'Upcoming' : 'Missed';
            }
          }
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: 'Date',
            font: {
              size: 14,
              weight: 'bold'
            }
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45
          }
        },
        y: {
          beginAtZero: true,
          max: 1,
          ticks: {
            callback: (value) => value === 1 ? 'Taken' : value === -1 ? 'Upcoming' : 'Missed',
            stepSize: 1
          },
          title: {
            display: true,
            text: 'Status',
            font: {
              size: 14,
              weight: 'bold'
            }
          }
        }
      },
      layout: {
        padding: 20
      }
    };

    const config: ChartConfiguration = {
      type: 'line',
      data: chartData,
      options: options
    };

    const chart2 = new Chart(ctx2, config);

    // return qs(".chartsBox")!;
  } catch (err) {
    console.error("Error fetching data: ", err);
    const error = '<div class="error">Error loading Component</div>'
    insertElement({ parent: props.parent, child: error, position: "beforeend" });
  };
};


import { qs } from "../selectors";
import { ComponentProps } from "../types"
import { datetimeFormatter, fetchAdherenceData, insertElement } from "../utils";
import { Chart, ChartConfiguration, ChartData, ChartOptions } from 'chart.js/auto';


export default async (props: ComponentProps): Promise<Element | undefined> => {
  const adherenceReportHTML = `
          <h1 style="text-align: center;">Medication Adherence Report</h1>
          <div class="adherence-container">
            <canvas id="adherence-chart" width="400" height="200"></canvas>
          </div>
        `;

  const data = await fetchAdherenceData();
  console.log(data);
  let chart: Chart | null = null
  const labels = data.map(entry => datetimeFormatter.format(new Date(entry.datetime)));
  const adherenceValues = data.map(entry => entry.adherence_status === 'fully_adherent' ? 1 : 0);  // 1 for taken, 0 for missed

  insertElement({ parent: props.parent, child: adherenceReportHTML, position: "beforeend" })

  const ctx = qs<HTMLCanvasElement>("#adherence-chart")!.getContext("2d");

  if (!ctx) {
    console.log("Could not acquire context");
    return;
  };

  const chartData: ChartData = {
    labels: labels,
    datasets: [{
      label: 'Adherence',
      data: adherenceValues,
      borderColor: 'rgba(75, 192, 192, 1)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
      borderWidth: 2,
      pointBackgroundColor: data.map(item =>
        item.adherence_status === 'completed' ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 99, 132, 1)'
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
            return context.parsed.y === 1 ? 'Taken' : 'Missed';
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
          callback: (value) => value === 1 ? 'Taken' : 'Missed',
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

  try {
    chart = new Chart(ctx, config);
  } catch (error) {
    console.error('Error creating chart:', error);
  }
};

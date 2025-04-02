import { qs } from "../selectors";
import { ComponentProps } from "../types"
import { fetchAdherenceData, insertElement } from "../utils";
import { Chart, ChartConfiguration, ChartData, ChartDataset, ChartOptions } from 'chart.js/auto';


export default async (props: ComponentProps): Promise<Element | undefined> => {
  const adherenceReportHTML = `
          <h2>Medication Adherence Report</h2>
          <canvas id="adherence-chart" width="400" height="200"></canvas>
        `;

  const data = await fetchAdherenceData();
  console.log(data);
  let chart: Chart | null = null
  const labels = data.map(entry => `${new Date(entry.datetime).toLocaleString()}`);
  const adherenceValues = data.map(entry => entry.adherence_status === 'completed' ? 1 : 0);  // 1 for taken, 0 for missed

  insertElement({ parent: props.parent, child: adherenceReportHTML, position: "beforeend" })

  const ctx = qs<HTMLCanvasElement>("#adherence-chart")!.getContext("2d");

  if (!ctx) {
    console.log("Could not acquire context");
    return;
  };

  const sortedData = [...data].sort((a, b) => new Date(a.datetime).getTime() - new Date(b.datetime).getTime());

  const dataset: ChartDataset<'line', { x: string; y: number }[]> = {
    label: 'Adherence',
    data: sortedData.map(item => ({ x: item.datetime, y: item.adherence_status === "completed" ? 1 : 0 })),
    borderColor: 'rgb(75, 192, 192)',
    backgroundColor: 'rgba(75, 192, 192, 0.5)',
    pointBackgroundColor: sortedData.map(item =>
      item.adherence_status === null ? 'red' :
        item.adherence_status === "partially_adherent" ? 'yellow' :
          'green'
    ),
    pointRadius: 6,
    pointHoverRadius: 8,
  };

  const config: ChartConfiguration<'line'> = {
    type: 'line',
    data: {
      datasets: [dataset]
    },
    options: {
      responsive: true,
      scales: {
        x: {
          type: 'time',
          time: {
            unit: 'day',
            displayFormats: {
              day: 'MMM d'
            }
          },
          title: {
            display: true,
            text: 'Date'
          }
        },
        y: {
          beginAtZero: true,
          max: 2,
          ticks: {
            stepSize: 1,
            callback: (value) => {
              switch (value) {
                case 0: return 'Missed';
                case 1: return 'Partial';
                case 2: return 'Full';
                default: return '';
              }
            }
          },
          title: {
            display: true,
            text: 'Adherence Level'
          }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: (context) => {
              const level = context.parsed.y;
              return `Adherence: ${level === 0 ? 'Missed' : level === 1 ? 'Partial' : 'Full'}`;
            }
          }
        }
      }
    }
  };

  try {
    chart = new Chart(ctx, config);
  } catch (error) {
    console.error('Error creating chart:', error);
  }
}

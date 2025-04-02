import { qs } from "../selectors";
import { AdherenceModel, ComponentProps } from "../types"
import { fetchAdherenceData, insertElement } from "../utils";


export default async (props: ComponentProps): Promise<Element | undefined> => {
  const adherenceReportHTML = `
          <h1>Medication Adherence Report</h1>
          <canvas id="adherence-chart" width="400" height="200"></canvas>
        `;

  const data = await fetchAdherenceData();
  console.log(data);

  insertElement({ parent: props.parent, child: adherenceReportHTML, position: "beforeend" })

  const canvas = qs<HTMLCanvasElement>("#adherence-chart")!;

  interface VisualizationConfig {
    cellSize: number;
    padding: number;
  }

  // Usage
  const visualization = createAdherenceVisualization(canvas, {
    cellSize: 30,
    padding: 10
  });

  try {
    visualization?.setData(data);
    visualization?.draw();
  } catch (error) {
    console.error('Error fetching adherence data:', error);
  }
};


function createAdherenceVisualization(canvas: HTMLCanvasElement, config: VisualizationConfig) {
  const ctx = canvas.getContext("2d")!;

  if (!ctx) return;

  let data: AdherenceModel[] = [];

  function setData(newData: AdherenceModel[]): void {
    data = newData;
  }

  function draw(): void {
    const daysInMonth = new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0).getDate();
    const startDate = new Date(new Date().getFullYear(), new Date().getMonth(), 1);

    canvas.width = (config.cellSize + config.padding) * 7 + config.padding;
    canvas.height = (config.cellSize + config.padding) * Math.ceil(daysInMonth / 7) + config.padding;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const dayStatuses = processData(startDate, daysInMonth);

    for (let i = 0; i < daysInMonth; i++) {
      const col = (i + startDate.getDay()) % 7;
      const row = Math.floor((i + startDate.getDay()) / 7);
      const x = col * (config.cellSize + config.padding) + config.padding;
      const y = row * (config.cellSize + config.padding) + config.padding;

      drawDay(x, y, i + 1, dayStatuses[i].status);
    }
  }

  function processData(startDate: Date, daysInMonth: number) {
    const dayStatuses = [];

    for (let i = 0; i < daysInMonth; i++) {
      const currentDate = new Date(startDate.getFullYear(), startDate.getMonth(), i + 1);
      const adherenceEntry = data.find(entry => {
        const entryDate = new Date(entry.datetime);
        return entryDate.getDate() === currentDate.getDate() &&
          entryDate.getMonth() === currentDate.getMonth() &&
          entryDate.getFullYear() === currentDate.getFullYear();
      });

      dayStatuses.push({
        date: currentDate,
        status: adherenceEntry ? adherenceEntry.adherence_status : 'not_adherent'
      });
    }

    return dayStatuses;
  }

  function drawDay(x: number, y: number, day: number, status: any): void {
    ctx.fillStyle = getStatusColor(status);
    ctx.fillRect(x, y, config.cellSize, config.cellSize);

    ctx.fillStyle = 'black';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(day.toString(), x + config.cellSize / 2, y + config.cellSize / 2);
  }

  function getStatusColor(status: any): string {
    switch (status) {
      case 'fully_adherent':
        return '#4CAF50';
      case 'partially_adherent':
        return '#F44336';
      case 'not_adherent':
      default:
        return '#9E9E9E';
    }
  }

  return {
    setData,
    draw
  };
}

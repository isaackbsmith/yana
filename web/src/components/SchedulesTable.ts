import apiRoutes from "../apiRoutes";
import { Pages } from "../routes";
import { qs } from "../selectors";
import { ComponentProps, ScheduleModel } from "../types";
import { formatDate, formatTime, insertElement, renderPage } from "../utils";


export default async (props: ComponentProps): Promise<Element | undefined> => {
  try {
    const response = await fetch(apiRoutes.GET_SCHEDULES);

    if (!response.ok) {
      throw new Error("Failed to fetch medication");
    }

    const schedules = await response.json() as ScheduleModel[];
    console.log(schedules)

    const schedulesTableHTML = `
      <div class="details medications-table">
        <div class="recentOrders">
          <div class="cardHeader">
              <h2>Your Schedules</h2>
              <a href="#" class="btn new-schedule-btn">New Schedule</a>
          </div>
          ${schedules.length > 0 ? `
          <table>
            <thead>
              <tr>
                <td>Date & Time</td>
                <td>Schedule Type</td>
                <td>Repeated</td>
                <td>Medication/Appointment</td>
              </tr>
            </thead>
            <tbody> 
              ${schedules.map((schedule) => (`
              <tr>
                <td>${formatDate(schedule.begin_date)} ${formatTime(schedule.begin_time)}</td>
                <td>${schedule.schedule_type}</td>
                <td>${schedule.repeated ? schedule.repeated : `Does not repeat`}</td>
                <td>${schedule.medication ? schedule.medication : schedule.appointment}</td>
              </tr>
            `)).join("")}
            </tbody>
          </table>
          ` : `<span class="empty-table-indicator">You have not created any schedule</span>`}
        </div>
      </div>
      `

    insertElement({ parent: props.parent, child: schedulesTableHTML, position: "beforeend" });

    const newScheduleBtn = qs(".new-schedule-btn")!;

    newScheduleBtn.addEventListener("click", () => {
      renderPage(Pages.NEW_SCHEDULE)
    })

    return qs(".schedules-table")!;
  } catch (err) {
    console.error("Error fetching data: ", err);
    const error = '<div class="error">Error loading schedule form</div>'
    insertElement({ parent: props.parent, child: error, position: "beforeend" });
  };
};

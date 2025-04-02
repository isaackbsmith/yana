import apiRoutes from "../apiRoutes";
import { Pages } from "../routes";
import { qs } from "../selectors";
import { AppointmentModel, ComponentProps } from "../types";
import { insertElement, renderPage } from "../utils";


export default async (props: ComponentProps): Promise<Element | undefined> => {
  try {
    const response = await fetch(apiRoutes.GET_APPOINTMENTS);

    if (!response.ok) {
      throw new Error("Failed to fetch appointments");
    }

    const appointments = await response.json() as AppointmentModel[];
    console.log(appointments)

    const appointmentsTableHTML = `
      <div class="details appointments-table">
        <div class="recentOrders">
          <div class="cardHeader">
              <h2>Your Appointments</h2>
              <a href="#" class="btn new-appointment-btn">New Appointment</a>
          </div>
          ${appointments.length > 0 ? `
          <table>
            <thead>
              <tr>
                <td>Reason</td>
                <td>Location</td>
              </tr>
            </thead>
            <tbody>
              ${appointments.map((appointment) => (`
              <tr>
                <td>${appointment.reason}</td>
                <td>${appointment.location}</td>
              </tr>
              `)).join("")}
            </tbody>
          </table>
          ` : `<span class="empty-table-indicator">You have not created any appointment</span>`}
        </div>
      </div>
      `
    insertElement({ parent: props.parent, child: appointmentsTableHTML, position: "beforeend" });

    const newMedicationBtn = qs(".new-appointment-btn")!;

    newMedicationBtn.addEventListener("click", () => {
      renderPage(Pages.NEW_APPOINTMENT);
    })

    return qs(".appointments-table")!;
  } catch (err) {
    console.error("Error fetching data: ", err);
    const error = '<div class="error">Error loading schedule form</div>'
    insertElement({ parent: props.parent, child: error, position: "beforeend" });
  };
};

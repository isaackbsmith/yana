import apiRoutes from "../apiRoutes";
import { qs } from "../selectors";
import { ComponentProps } from "../types"
import { insertElement } from "../utils";


export default async (props: ComponentProps): Promise<Element | undefined> => {
  const createAppointmentHTML = `
          <section class="entity-creation">
              <h2>Create New Appointment</h2>
              <form id="appointment-form" class="form">
                  <div class="form-group">
                      <label for="description">Reason:</label>
                      <textarea id="reason" name="reason" rows="2" placeholder="Eg. Annual physical check-up" required></textarea>
                  </div>
                  <div class="form-group">
                      <label for="location">Location:</label>
                      <input type="text" id="location" name="location" placeholder="Eg. City Hospital, 101 River Avenue">
                  </div>
                  <button type="submit" class="btn btn-primary">Create Appointment</button>
              </form>
          </section>
        `;

  try {
    insertElement({ parent: props.parent, child: createAppointmentHTML, position: "beforeend" });

    const appointmentForm = qs<HTMLFormElement>("#appointment-form")!;
    appointmentForm.addEventListener("submit", handleAppointmentSubmit);

    return qs(".entity-creation")!;
  } catch (err) {
    console.error("Error occurred: ", err);
    const error = '<div class="error">Error</div>'
    insertElement({ parent: props.parent, child: error, position: "beforeend" });
  }
};

async function handleAppointmentSubmit(event: SubmitEvent) {
  event.preventDefault();
  const form = event.target as HTMLFormElement;
  const formData = new FormData(form);
  const appointmentData = Object.fromEntries(formData.entries());
  console.log(appointmentData)

  try {
    const response = await fetch(apiRoutes.ADD_APPOINTMENT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(appointmentData),
    });

    if (response.ok) {
      alert("Appointment created successfully!");
      form.reset();
    } else {
      throw new Error("Failed to create appointment");
    }
  } catch (error) {
    console.error("Error creating appointment:", error);
    alert("Failed to create appointment. Please try again.");
  }
}

import apiRoutes from "../apiRoutes";
import { qs } from "../selectors";
import { MedicationModel, ComponentProps, AppointmentModel, NewScheduleModel } from "../types";
import { fetchAppointments, fetchMedications, insertElement } from "../utils";


export default async (props: ComponentProps): Promise<Element | undefined> => {
  const createScheduleHTML = `
          <section class="schedule-creation">
              <h2>Create Medication or Appointment Schedule</h2>
              <form id="schedule-form" class="form">
                  <div class="form-group">
                      <label for="begin_date">Begin Date:</label>
                      <input type="date" value=${new Date().toISOString().slice(0, 10)} id="begin_date" name="begin_date" required>
                  </div>
                  <div class="form-group">
                      <label for="end_date">End Date:</label>
                      <input type="date" id="end_date" name="end_date">
                  </div>
                  <div class="form-group">
                      <label for="begin_time">Begin Time:</label>
                      <input type="time" value="06:00" id="begin_time" name="begin_time" required>
                  </div>
                  <div class="form-group">
                      <label for="end_time">End Time:</label>
                      <input type="time" id="end_time" name="end_time">
                  </div>
                  <div class="form-group">
                      <label for="schedule_type">Schedule Type:</label>
                      <select id="schedule_type" name="schedule_type" required>
                          <option value="medication">Medication</option>
                          <option value="appointment">Appointment</option>
                      </select>
                  </div>
                  <div class="form-group">
                      <label for="medication_id">Medication:</label>
                      <select id="medication_id" name="medication_id">
                          <option value="">Select a medication</option>
                          <!-- This will be populated dynamically -->
                      </select>
                  </div>
                  <div class="form-group" style="display: none;">
                      <label for="appointment_id">Appointment:</label>
                      <select id="appointment_id" name="appointment_id">
                          <option value="">Select an appointment</option>
                          <!-- This will be populated dynamically -->
                      </select>
                  </div>
                  <div class="form-group">
                      <label for="repeated">Repeat:</label>
                      <select id="repeated" name="repeated">
                          <option value="">Select a repetition type</option>
                          <option value="minutely">Minutely</option>
                          <option value="hourly">Hourly</option>
                          <option value="daily">Daily</option>
                          <option value="weekly">Weekly</option>
                          <option value="monthly">Monthly</option>
                          <option value="annualy">Yearly</option>
                      </select>
                  </div>
                  <div class="form-group" style="display: none;">
                      <label for="repeated_monthly_on">Repeat Monthly On:</label>
                      <select id="repeated_monthly_on" name="repeated_monthly_on">
                          <option value="">Select an option</option>
                          <option value="same_day">Same Day</option>
                          <option value="same_weekday">Same Weekday</option>
                      </select>
                  </div>
                  <div class="form-group">
                      <label for="repetition_step">Repetition Step:</label>
                      <input type="number" value=1 id="repetition_step" name="repetition_step" min="1">
                  </div>
                  <div class="form-group">
                      <label for="repeated_until">Repeat Until:</label>
                      <select id="repeated_until" name="repeated_until">
                          <option value="">Select an option</option>
                          <option value="forever">Forever</option>
                          <option value="until_date">Specific Date</option>
                          <option value="n_repetitions">Number of Repetitions</option>
                      </select>
                  </div>
                  <div class="form-group" id="repeated_until_date_group" style="display: none;">
                      <label for="repeated_until_date">Repeat Until Date:</label>
                      <input type="date" id="repeated_until_date" name="repeated_until_date">
                  </div>
                  <div class="form-group" id="repeated_reps_group" style="display: none;">
                      <label for="repeated_reps">Number of Repetitions:</label>
                      <input type="number" id="repeated_reps" name="repeated_reps" min="1">
                  </div>
                  <button type="submit" class="btn btn-primary">Create Schedule</button>
              </form>
          </section>
      </div>
`;

  try {
    insertElement({ parent: props.parent, child: createScheduleHTML, position: "beforeend" });

    // Add event listeners and form handling logic
    const scheduleForm = qs<HTMLFormElement>("#schedule-form")!;
    scheduleForm.addEventListener("submit", handleScheduleSubmit);

    // Add event listeners for dynamic form fields
    const repeatedSelect = qs<HTMLSelectElement>("#repeated")!;
    const repeatedUntilSelect = qs<HTMLSelectElement>("#repeated_until")!;
    const scheduleTypeSelect = qs<HTMLSelectElement>("#schedule_type")!;

    repeatedSelect.addEventListener("change", toggleRepeatOptions);
    repeatedUntilSelect.addEventListener("change", toggleRepeatedUntilOptions);
    scheduleTypeSelect.addEventListener("change", toggleMedicationOrAppointment);

    // Populate medications initially
    const medications = await fetchMedications();
    populateMedicationSelect(medications);

    return qs(".entity-creation")!;
  } catch (err) {
    console.error("Error fetching data: ", err);
    const error = '<div class="error">Error loading schedule form</div>'
    insertElement({ parent: props.parent, child: error, position: "beforeend" });
  };
};

const handleScheduleSubmit = async (event: SubmitEvent) => {
  event.preventDefault();
  const form = event.target as HTMLFormElement;
  const formData = new FormData(form);
  const scheduleData: NewScheduleModel = {
    begin_date: formData.get("begin_date") as string,
    end_date: formData.get("end_date") === "" ? null : formData.get("end_date") as string,
    begin_time: formData.get("begin_time") as string,
    end_time: formData.get("end_time") === "" ? null : formData.get("end_time") as string,
    schedule_type: formData.get("schedule_type") as string,
    repeated: formData.get("repeated") === "" ? null : formData.get("repeated") as string,
    repetition_step: Number(formData.get("repetition_step")),
    repeated_monthly_on: formData.get("repeated_monthly_on") === "" ? null : formData.get("repeated_monthly_on") as string,
    repeated_until: formData.get("repeated_until") === "" ? null : formData.get("repeated_until") as string,
    repeated_until_date: formData.get("repeated_until_date") === "" ? null : formData.get("repeated_until_date") as string,
    repeated_reps: Number(formData.get("repeated_reps")) === 0 ? null : Number(formData.get("repeated_reps")),
    medication_id: formData.get("medication_id") === "" ? null : formData.get("medication_id") as string,
    appointment_id: formData.get("appointment_id") === "" ? null : formData.get("appointment_id") as string,
  }

  // Validations
  // Validate date and time logic
  if ((scheduleData.begin_date && scheduleData.end_date) && (scheduleData.begin_date > scheduleData.end_date)) {
    alert("Begin date cannot be after end date");
    return;
  }

  if ((scheduleData.begin_time && scheduleData.end_time) && (scheduleData.begin_time > scheduleData.end_time)) {
    alert("Begin time cannot be greater than end time")
  };

  // Check wheather medication is selected
  if (scheduleData.schedule_type == "medication" && !scheduleData.medication_id) {
    alert("Please choose a medication to create a schedule for");
    return
  }

  // Check wheather appointment is selected
  if (scheduleData.schedule_type == "appointment" && !scheduleData.appointment_id) {
    alert("Please choose an appointment to create a schedule for");
    return;
  }

  // Check wheather repeated if so, repeated_until must be set
  if (scheduleData.repeated) {
    if (scheduleData.repeated == "monthly" && !scheduleData.repeated_monthly_on) {
      alert("You must set the monthly repetition type (hint: Repeat Monthly On)");
      return;
    };

    if (!scheduleData.repeated_until) {
      alert("You must set the duration of the repetitions (hint: Repeat Until)");
      return;
    };

    if (scheduleData.repeated_until == "until_date" && !scheduleData.repeated_until_date) {
      alert("You must set an end date for the repeat duration (hint: Repeat Until Date)");
      return;
    };

    if (scheduleData.repeated_until == "n_repetitions" && !scheduleData.repeated_reps) {
      alert("You must set the number of repetitions for the schedule (hint: Number of Repetitions)")
      return;
    };
  } else if (scheduleData.repeated_until) {
    alert("Your schedule does not repeat. Set it to repeat (Hint: Repeat)")
    return;
  };

  console.log(scheduleData);

  try {
    const response = await fetch(apiRoutes.ADD_SCHEDULE, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(scheduleData),
    });

    if (response.ok) {
      alert("Schedule created successfully!");
      // location.reload();
      form.reset();
    } else {
      throw new Error("Failed to create schedule");
    }
  } catch (error) {
    console.error("Error creating schedule:", error);
    alert("Failed to create schedule. Please try again.");
  }
}

const populateMedicationSelect = (medications: MedicationModel[]) => {
  const medicationSelect = qs("#medication_id")!;
  medicationSelect.innerHTML = '<option value="">Select a medication</option>';
  medications.forEach((medication: MedicationModel) => {
    const option = document.createElement("option");
    option.value = medication.id;
    option.textContent = `${medication.brand_name} (${medication.generic_name})`;
    medicationSelect.appendChild(option);
  });
}

const populateAppointmentSelect = (appointments: AppointmentModel[]) => {
  const medicationSelect = qs("#appointment_id")!;
  medicationSelect.innerHTML = '<option value="">Select an appointment</option>';
  appointments.forEach((appointment) => {
    const option = document.createElement("option");
    option.value = appointment.id;
    option.textContent = `${appointment.reason}`;
    medicationSelect.appendChild(option);
  });
}

function toggleRepeatOptions(this: HTMLSelectElement) {
  const repeatedValue = this.value;
  const repeatedUntilGroup = qs<HTMLSelectElement>("#repeated_until")!.closest(".form-group")! as HTMLDivElement;;
  const repeatedMonthlyOnSelect = qs<HTMLSelectElement>("#repeated_monthly_on")!
  const repeatedMonthlyOnGroup = repeatedMonthlyOnSelect.closest(".form-group")! as HTMLDivElement;

  // reset everything after every change
  if (repeatedValue) {
    repeatedUntilGroup.style.display = "block";
    if (repeatedValue === "monthly") {
      repeatedMonthlyOnGroup.style.display = "block";
    } else {
      repeatedMonthlyOnSelect.value = "";
      repeatedMonthlyOnGroup.style.display = "none";
    }
  } else {
    repeatedUntilGroup.style.display = "none";
    repeatedMonthlyOnGroup.style.display = "none";
    repeatedMonthlyOnSelect.value = "";
  }
}

async function toggleMedicationOrAppointment(this: HTMLSelectElement) {
  const scheduleType = this.value;
  const medicationsGroup = qs("#medication_id")!.closest(".form-group") as HTMLDivElement;
  const appointmentsGroup = qs("#appointment_id")!.closest(".form-group") as HTMLDivElement;

  try {
    if (scheduleType == "medication") {
      appointmentsGroup.style.display = "none";
      medicationsGroup.style.display = "block";
      const medications = await fetchMedications()
      populateMedicationSelect(medications);
    } else if (scheduleType == "appointment") {
      medicationsGroup.style.display = "none";
      appointmentsGroup.style.display = "block";
      const appointments = await fetchAppointments();
      populateAppointmentSelect(appointments);
    } else {
      medicationsGroup.style.display = "none";
      appointmentsGroup.style.display = "none";
    };
  } catch (err) {
    throw new Error("Error loading data")
  };
};

function toggleRepeatedUntilOptions(this: HTMLSelectElement) {
  const repeatedUntilValue = this.value;
  const repeatedUntilDateGroup = qs<HTMLDivElement>("#repeated_until_date_group")!;
  const repeatedRepsGroup = qs<HTMLDivElement>("#repeated_reps_group")!;

  if (repeatedUntilValue === "until_date") {
    repeatedUntilDateGroup.style.display = "block";
    repeatedRepsGroup.style.display = "none";
  } else if (repeatedUntilValue === "n_repetitions") {
    repeatedUntilDateGroup.style.display = "none";
    repeatedRepsGroup.style.display = "block";
  } else {
    repeatedUntilDateGroup.style.display = "none";
    repeatedRepsGroup.style.display = "none";
  }
}


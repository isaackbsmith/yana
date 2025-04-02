export function renderMedication() {
  const mainContent = document.getElementById("main-content");

  const medicationHTML = `
        <h1>Medication Management</h1>
        <div class="medication-container">
            <section class="medication-creation">
                <h2>Create New Medication</h2>
                <form id="medication-form" class="form">
                    <div class="form-group">
                        <label for="generic_name">Generic Name:</label>
                        <input type="text" id="generic_name" name="generic_name" required>
                    </div>
                    <div class="form-group">
                        <label for="brand_name">Brand Name:</label>
                        <input type="text" id="brand_name" name="brand_name" required>
                    </div>
                    <div class="form-group">
                        <label for="description">Description:</label>
                        <textarea id="description" name="description" rows="3" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="strength">Strength:</label>
                        <input type="text" id="strength" name="strength" required>
                    </div>
                    <div class="form-group">
                        <label for="dosage">Dosage:</label>
                        <input type="number" id="dosage" name="dosage" required>
                    </div>
                    <div class="form-group">
                        <label for="dosage_form_id">Dosage Form:</label>
                        <select id="dosage_form_id" name="dosage_form_id" required>
                            <option value="">Select a dosage form</option>
                            <option value="1">Tablet</option>
                            <option value="2">Capsule</option>
                            <option value="3">Liquid</option>
                            <option value="4">Injection</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="medication_route_id">Medication Route:</label>
                        <select id="medication_route_id" name="medication_route_id" required>
                            <option value="">Select a medication route</option>
                            <option value="1">Oral</option>
                            <option value="2">Topical</option>
                            <option value="3">Intravenous</option>
                            <option value="4">Intramuscular</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">Create Medication</button>
                </form>
            </section>

            <section class="schedule-creation">
                <h2>Create Medication Schedule</h2>
                <form id="schedule-form" class="form">
                    <div class="form-group">
                        <label for="begin_date">Begin Date:</label>
                        <input type="date" id="begin_date" name="begin_date" required>
                    </div>
                    <div class="form-group">
                        <label for="end_date">End Date:</label>
                        <input type="date" id="end_date" name="end_date" required>
                    </div>
                    <div class="form-group">
                        <label for="begin_time">Begin Time:</label>
                        <input type="time" id="begin_time" name="begin_time" required>
                    </div>
                    <div class="form-group">
                        <label for="end_time">End Time:</label>
                        <input type="time" id="end_time" name="end_time">
                    </div>
                    <div class="form-group">
                        <label for="schedule_type">Schedule Type:</label>
                        <select id="schedule_type" name="schedule_type" required>
                            <option value="">Select a schedule type</option>
                            <option value="daily">Daily</option>
                            <option value="weekly">Weekly</option>
                            <option value="monthly">Monthly</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="medication_id">Medication:</label>
                        <select id="medication_id" name="medication_id" required>
                            <option value="">Select a medication</option>
                            <!-- This will be populated dynamically -->
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="repeated">Repeat:</label>
                        <select id="repeated" name="repeated">
                            <option value="">No repeat</option>
                            <option value="daily">Daily</option>
                            <option value="weekly">Weekly</option>
                            <option value="monthly">Monthly</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="repetition_step">Repetition Step:</label>
                        <input type="number" id="repetition_step" name="repetition_step" min="1">
                    </div>
                    <div class="form-group">
                        <label for="repeated_until">Repeat Until:</label>
                        <select id="repeated_until" name="repeated_until">
                            <option value="">Select an option</option>
                            <option value="date">Specific Date</option>
                            <option value="occurrences">Number of Occurrences</option>
                        </select>
                    </div>
                    <div class="form-group" id="repeated_until_date_group" style="display: none;">
                        <label for="repeated_until_date">Repeat Until Date:</label>
                        <input type="date" id="repeated_until_date" name="repeated_until_date">
                    </div>
                    <div class="form-group" id="repeated_reps_group" style="display: none;">
                        <label for="repeated_reps">Number of Occurrences:</label>
                        <input type="number" id="repeated_reps" name="repeated_reps" min="1">
                    </div>
                    <div class="form-group" id="days_of_week_group" style="display: none;">
                        <fieldset>
                            <legend>Days of Week:</legend>
                            <div class="checkbox-group">
                                <input type="checkbox" id="monday" name="days_of_week" value="monday">
                                <label for="monday">Monday</label>
                            </div>
                            <div class="checkbox-group">
                                <input type="checkbox" id="tuesday" name="days_of_week" value="tuesday">
                                <label for="tuesday">Tuesday</label>
                            </div>
                            <div class="checkbox-group">
                                <input type="checkbox" id="wednesday" name="days_of_week" value="wednesday">
                                <label for="wednesday">Wednesday</label>
                            </div>
                            <div class="checkbox-group">
                                <input type="checkbox" id="thursday" name="days_of_week" value="thursday">
                                <label for="thursday">Thursday</label>
                            </div>
                            <div class="checkbox-group">
                                <input type="checkbox" id="friday" name="days_of_week" value="friday">
                                <label for="friday">Friday</label>
                            </div>
                            <div class="checkbox-group">
                                <input type="checkbox" id="saturday" name="days_of_week" value="saturday">
                                <label for="saturday">Saturday</label>
                            </div>
                            <div class="checkbox-group">
                                <input type="checkbox" id="sunday" name="days_of_week" value="sunday">
                                <label for="sunday">Sunday</label>
                            </div>
                        </fieldset>
                    </div>
                    <button type="submit" class="btn btn-primary">Create Schedule</button>
                </form>
            </section>
        </div>
    `;

  mainContent.innerHTML = medicationHTML;

  // Add event listeners and form handling logic
  const medicationForm = document.getElementById("medication-form");
  const scheduleForm = document.getElementById("schedule-form");

  medicationForm.addEventListener("submit", handleMedicationSubmit);
  scheduleForm.addEventListener("submit", handleScheduleSubmit);

  // Add event listeners for dynamic form fields
  const repeatedSelect = document.getElementById("repeated");
  const repeatedUntilSelect = document.getElementById("repeated_until");
  const scheduleTypeSelect = document.getElementById("schedule_type");

  repeatedSelect.addEventListener("change", toggleRepeatOptions);
  repeatedUntilSelect.addEventListener("change", toggleRepeatedUntilOptions);
  scheduleTypeSelect.addEventListener("change", toggleDaysOfWeek);

  // Fetch and populate medications for the schedule form
  fetchMedications();
}

async function handleMedicationSubmit(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const medicationData = Object.fromEntries(formData.entries());

  try {
    const response = await fetch("/api/medications", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(medicationData),
    });

    if (response.ok) {
      alert("Medication created successfully!");
      event.target.reset();
      fetchMedications(); // Refresh the medications list
    } else {
      throw new Error("Failed to create medication");
    }
  } catch (error) {
    console.error("Error creating medication:", error);
    alert("Failed to create medication. Please try again.");
  }
}

async function handleScheduleSubmit(event) {
  event.preventDefault();
  const formData = new FormData(event.target);
  const scheduleData = Object.fromEntries(formData.entries());

  // Handle days of week
  scheduleData.days_of_week = Array.from(formData.getAll("days_of_week"));

  // Convert date-time fields to ISO format
  scheduleData.begin_date = new Date(scheduleData.begin_date).toISOString();
  scheduleData.end_date = new Date(scheduleData.end_date).toISOString();
  scheduleData.begin_time = new Date(
    `1970-01-01T${scheduleData.begin_time}`,
  ).toISOString();
  scheduleData.end_time = scheduleData.end_time
    ? new Date(`1970-01-01T${scheduleData.end_time}`).toISOString()
    : null;

  // Handle repeated_until_date
  if (scheduleData.repeated_until === "date") {
    scheduleData.repeated_until_date = new Date(
      scheduleData.repeated_until_date,
    ).toISOString();
  } else {
    scheduleData.repeated_until_date = null;
  }

  // Remove unused fields
  if (scheduleData.repeated_until !== "occurrences") {
    delete scheduleData.repeated_reps;
  }

  try {
    const response = await fetch("/api/schedules", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(scheduleData),
    });

    if (response.ok) {
      alert("Schedule created successfully!");
      event.target.reset();
    } else {
      throw new Error("Failed to create schedule");
    }
  } catch (error) {
    console.error("Error creating schedule:", error);
    alert("Failed to create schedule. Please try again.");
  }
}

function toggleRepeatOptions() {
  const repeatedValue = this.value;
  const repeatedUntilGroup = document
    .getElementById("repeated_until")
    .closest(".form-group");
  const daysOfWeekGroup = document.getElementById("days_of_week_group");

  if (repeatedValue) {
    repeatedUntilGroup.style.display = "block";
    if (repeatedValue === "weekly") {
      daysOfWeekGroup.style.display = "block";
    } else {
      daysOfWeekGroup.style.display = "none";
    }
  } else {
    repeatedUntilGroup.style.display = "none";
    daysOfWeekGroup.style.display = "none";
  }
}

function toggleRepeatedUntilOptions() {
  const repeatedUntilValue = this.value;
  const repeatedUntilDateGroup = document.getElementById(
    "repeated_until_date_group",
  );
  const repeatedRepsGroup = document.getElementById("repeated_reps_group");

  if (repeatedUntilValue === "date") {
    repeatedUntilDateGroup.style.display = "block";
    repeatedRepsGroup.style.display = "none";
  } else if (repeatedUntilValue === "occurrences") {
    repeatedUntilDateGroup.style.display = "none";
    repeatedRepsGroup.style.display = "block";
  } else {
    repeatedUntilDateGroup.style.display = "none";
    repeatedRepsGroup.style.display = "none";
  }
}

function toggleDaysOfWeek() {
  const scheduleTypeValue = this.value;
  const daysOfWeekGroup = document.getElementById("days_of_week_group");

  if (scheduleTypeValue === "weekly") {
    daysOfWeekGroup.style.display = "block";
  } else {
    daysOfWeekGroup.style.display = "none";
  }
}

async function fetchMedications() {
  try {
    const response = await fetch("/api/medications");
    if (response.ok) {
      const medications = await response.json();
      populateMedicationSelect(medications);
    } else {
      throw new Error("Failed to fetch medications");
    }
  } catch (error) {
    console.error("Error fetching medications:", error);
  }
}

function populateMedicationSelect(medications) {
  const medicationSelect = document.getElementById("medication_id");
  medicationSelect.innerHTML = '<option value="">Select a medication</option>';
  medications.forEach((medication) => {
    const option = document.createElement("option");
    option.value = medication.id;
    option.textContent = `${medication.brand_name} (${medication.generic_name})`;
    medicationSelect.appendChild(option);
  });
}

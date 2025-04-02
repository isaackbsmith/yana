import apiRoutes from "../apiRoutes";
import { qs } from "../selectors";
import { DosageFormModel, MedicationRouteModel, ComponentProps, MedicationModel } from "../types"
import { fetchDosageForms, fetchMedicationRoutes, insertElement } from "../utils";


export default async (props: ComponentProps): Promise<Element | undefined> => {
    const med: MedicationModel = props.data?.medication;
    const createMedicationHTML = `
        <section class="entity-creation">
            <h2>Create New Medication</h2>
            <form id="medication-form" class="form">
                <div class="form-group">
                    <label for="brand_name">Brand Name:</label>
                    <input
                        type="text"
                        id="brand_name"
                        name="brand_name"
                        placeholder="Eg. Panadol"
                        required
                        value=${med ? med.brand_name : ''}
                    >
                </div>
                <div class="form-group">
                    <label for="generic_name">Generic Name:</label>
                    <input type="text" id="generic_name" name="generic_name" placeholder="Eg. Paracetamol" required>
                </div>
                <div class="form-group">
                    <label for="description">Description:</label>
                    <textarea id="description" name="description" rows="2" placeholder="Eg. For relief and fever reduction" required></textarea>
                </div>
                <div class="form-group">
                    <label for="strength">Strength:</label>
                    <input type="text" id="strength" name="strength" placeholder="500 mg/milligrams" required>
                </div>
                <div class="form-group">
                    <label for="dosage">Dosage:</label>
                    <input type="number" id="dosage" name="dosage" value=1 min=1 required>
                </div>
                <div class="form-group">
                    <label for="dosage_form_id">Dosage Form:</label>
                    <select id="dosage_form_id" name="dosage_form_id" required>
                        <option value="">Select a dosage form</option>
                        <!-- This will be populated dynamically -->
                    </select>
                </div>
                <div class="form-group">
                    <label for="medication_route_id">Medication Route:</label>
                    <select id="medication_route_id" name="medication_route_id" required>
                        <option value="">Select a medication route</option>
                        <!-- This will be populated dynamically -->
                    </select>
                </div>
                <button type="submit" class="btn btn-primary">Create Medication</button>
            </form>
        </section>
            `

    try {
        const [medicationRoutes, dosageForms] = await Promise.all([
            fetchMedicationRoutes(),
            fetchDosageForms()
        ]);

        insertElement({ parent: props.parent, child: createMedicationHTML, position: "beforeend" });

        // Add event listeners and form handling logic
        const medicationForm = qs<HTMLFormElement>("#medication-form")!;
        medicationForm.addEventListener("submit", handleMedicationSubmit);

        // Populate the data in the form
        populateMedicationRoutesSelect(medicationRoutes);
        populateDosageFormsSelect(dosageForms)

        // return a reference to self (parent element)
        return qs(".entity-creation")!;
    } catch (err) {
        console.error("Error fetching medication: ", err);
        const error = '<div class="error">Error loading Medications</div>'
        insertElement({ parent: props.parent, child: error, position: "beforeend" });
    }
};

const populateDosageFormsSelect = (routes: DosageFormModel[]) => {
    const medicationRouteSelect = qs("#dosage_form_id")!;
    medicationRouteSelect.innerHTML = '<option value="">Select a dosage form</option>';
    routes.forEach((route) => {
        const option = document.createElement("option");
        option.value = route.id;
        option.textContent = `${route.name} (${route.friendly_name})`;
        medicationRouteSelect.appendChild(option);
    });
}

const populateMedicationRoutesSelect = (routes: MedicationRouteModel[]) => {
    const medicationRouteSelect = qs("#medication_route_id")!;
    medicationRouteSelect.innerHTML = '<option value="">Select a medication route</option>';
    routes.forEach((route) => {
        const option = document.createElement("option");
        option.value = route.id;
        option.textContent = `${route.name} (${route.friendly_name})`;
        medicationRouteSelect.appendChild(option);
    });
}

async function handleMedicationSubmit(event: SubmitEvent) {
    event.preventDefault();
    const form = event.target as HTMLFormElement;
    const formData = new FormData(form);
    const medicationData = Object.fromEntries(formData.entries());
    console.log(medicationData)

    try {
        const response = await fetch(apiRoutes.ADD_MEDICATION, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(medicationData),
        });

        console.log("route: ", apiRoutes.ADD_MEDICATION)

        if (response.ok) {
            alert("Medication created successfully!");
            form.reset();
        } else {
            throw new Error("Failed to create medication");
        }
    } catch (error) {
        console.error("Error creating medication:", error);
        alert("Failed to create medication. Please try again.");
    }
}

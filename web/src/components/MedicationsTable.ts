import apiRoutes from "../apiRoutes";
import { Pages } from "../routes";
import { qs, qsa } from "../selectors";
import { ComponentProps, MedicationModel } from "../types";
import { insertElement, renderPage } from "../utils";


export default async (props: ComponentProps): Promise<Element | undefined> => {
  try {
    const response = await fetch(apiRoutes.GET_MEDICATIONS);

    if (!response.ok) {
      throw new Error("Failed to fetch medication");
    }

    const medications = await response.json() as MedicationModel[];

    const medicationsTableHTML = `
      <div class="details medications-table">
        <div class="recentOrders">
          <div class="cardHeader">
              <h2>Your Medications</h2>
              <a href="#" class="btn new-medication-btn">New Medication</a>
          </div>
          ${medications.length > 0 ? `
          <table>
            <thead>
              <tr>
                <td>Medication</td>
                <td>Strength</td>
                <td>Dosage + Form</td>
                <td>Description</td>
              </tr>
            </thead>
            <tbody>
              ${medications.map((medication) => (`
                <tr class="row-selectable" data-row-id=${medication.id}>
                  <td>${medication.brand_name} (${medication.generic_name})</td>
                  <td>${medication.strength}</td>
                  <td>${medication.dosage} ${medication.dosage_form}${medication.dosage > 1 ? 's' : ''}</td>
                  <td>${medication.description}</td>
                </tr>
              `)).join("")}
            </tbody>
          </table>
          ` : `<span class="empty-table-indicator">You have not created any medication</span>`}
        </div>
      </div>
      `
    insertElement({ parent: props.parent, child: medicationsTableHTML, position: "beforeend" });

    const newMedicationBtn = qs(".new-medication-btn")!;

    newMedicationBtn.addEventListener("click", () => {
      renderPage(Pages.NEW_MEDICATION);
    })

    const rows = qsa<HTMLTableRowElement>(".row-selectable")!;
    rows.forEach((row) => {
      row.addEventListener("click", () => {
        const id = row.getAttribute("data-row-id");
        if (!id) return;
        renderPage(Pages.EDIT_MEDICATION, { detail: { id } });
      })
    })

    return qs(".medications-table")!;
  } catch (err) {
    console.error("Error fetching data: ", err);
    const error = '<div class="error">Cannot load medications at this time. Try reloading</div>'
    insertElement({ parent: props.parent, child: error, position: "beforeend" });
  };
};

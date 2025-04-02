import CreateMedication from "../components/CreateMedication";
import Header from "../components/Header";
import { qs } from "../selectors";
import { Page, PageProps } from "../types";
import { fetchMedication, insertElement } from "../utils";

export default class implements Page {
	public async render(props: PageProps) {
		const loading = '<div class="loader">Loading dashboard ...</div>';
		insertElement({ parent: props.root, child: loading, position: "beforeend" });

		try {
			// Fetch data
			if (!props.nextPageData) {
				throw new Error("Medication id not provided")
			}

			const medication = await fetchMedication(props.nextPageData.detail.medication_id);

			// Remove the loading indicator
			qs(".loader")?.remove();

			// Compose elements
			Header({ parent: props.root, data: null });
			CreateMedication({ parent: props.root, data: { medication } })

		} catch (err) {
			console.error("Error fetching dashboard data: ", err);
			const error = '<div class="error">Error loading dashboard</div>'
			insertElement({ parent: props.root, child: error, position: "beforeend" });
		}
	}
};



import CreateMedication from "../components/CreateMedication";
import Header from "../components/Header";
import { qs } from "../selectors";
import { Page, PageProps } from "../types";
import { insertElement } from "../utils";

export default class implements Page {
	public render(props: PageProps) {
		const loading = '<div class="loader">Loading dashboard ...</div>';
		insertElement({ parent: props.root, child: loading, position: "beforeend" });

		try {
			// Fetch data

			// Remove the loading indicator
			qs(".loader")?.remove();

			// Compose elements
			Header({ parent: props.root, data: null });
			CreateMedication({ parent: props.root, data: null });

		} catch (err) {
			console.error("Error fetching dashboard data: ", err);
			const error = '<div class="error">Error loading dashboard</div>'
			insertElement({ parent: props.root, child: error, position: "beforeend" });
		}
	}
};



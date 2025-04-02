import CreateSchedule from "../components/CreateSchedule";
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

			qs(".loader")?.remove();

			Header({ parent: props.root, data: null });
			CreateSchedule({ parent: props.root, data: null })

		} catch (err) {
			console.error("Error fetching dashboard data: ", err);
			const error = '<div class="error">Error loading dashboard</div>'
			insertElement({ parent: props.root, child: error, position: "beforeend" });
		}
	}
};



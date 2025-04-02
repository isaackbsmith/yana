import { Page, ComposeElement, NextPageData, MedicationModel, AppointmentModel, PageProps, MedicationRouteModel, DosageFormModel, AdherenceModel } from "./types";
import NotFound from "./pages/NotFound";
import pageMap, { Pages } from "./routes";
import { qs } from "./selectors";
import apiRoutes from "./apiRoutes";

export const datetimeFormatter = new Intl.DateTimeFormat('en-GB', {
	year: 'numeric',
	month: 'short',
	day: 'numeric',
	hour: '2-digit',
	minute: '2-digit',
	hour12: false
});


export const formatTime = (time: string) => {
	return new Date(`1970-01-01T${time}`).toLocaleTimeString('en-GB', {
		hour: '2-digit',
		minute: '2-digit',
		hour12: true
	});
}

export const formatDate = (date: string) => {
	return new Date(date).toLocaleDateString('en-GB', {
		weekday: 'short',
		year: 'numeric',
		month: 'short',
		day: 'numeric'
	});
}


export const createElement = (htmlStr: string) => {
	const template = document.createElement("template")
	template.innerHTML = htmlStr.trim();
	return template.content.firstElementChild!;
};

export const getPageByName = (name: string): Page => {
	const Page = pageMap[name]
	if (Page) return Page
	return new NotFound()
};

export const renderPage = (page: Pages | null, data: NextPageData | null = null): void => {
	if (!page) return;

	// Do not navigate if same page
	const currentPage = qs<HTMLTitleElement>("title")!;
	if (page == currentPage.innerText) {
		return;
	};

	// Get the main content container
	const container = qs(".main")!;

	// Clear page and insert new title
	container.innerHTML = "";
	currentPage.innerText = page;

	console.log("Rendering page: ", page)
	const props: PageProps = {
		root: container,
		nextPageData: data,
	};
	getPageByName(page).render(props)
}

export const strToEnum = <T>(str: string, enumType: { [key: string]: T }): T | null => {
	for (const key in enumType) {
		if (enumType[key] == str) {
			return enumType[key];
		}
	}
	return null
}

export const insertElement = (composer: ComposeElement): void => {
	composer.parent.insertAdjacentHTML(composer.position, composer.child);
}

export const toggleSideNav = () => {
	const toggle = qs(".toggle");
	const sideNav = qs(".navigation");
	const mainContainer = qs(".main")!;

	toggle?.addEventListener("click", () => {
		console.log("nav toggled", sideNav);
		sideNav?.classList.toggle("active");
		mainContainer.classList.toggle("active");
	});
};


export const fetchMedications = async (): Promise<MedicationModel[]> => await (await fetch(apiRoutes.GET_MEDICATIONS)).json();

export const fetchMedication = async (medication_id: string): Promise<MedicationModel[]> => await (await fetch(`${apiRoutes.GET_MEDICATIONS}?medication_id=${medication_id}`)).json();

export const fetchAppointments = async (): Promise<AppointmentModel[]> => await (await fetch(apiRoutes.GET_APPOINTMENTS)).json();
export const fetchMedicationRoutes = async (): Promise<MedicationRouteModel[]> => await (await fetch(apiRoutes.GET_MEDICATION_ROUTES)).json();
export const fetchDosageForms = async (): Promise<DosageFormModel[]> => await (await fetch(apiRoutes.GET_DOSAGE_FORMS)).json();
export const fetchAdherenceData = async (): Promise<AdherenceModel[]> => await (await fetch(apiRoutes.GET_ADHERENCE_DATA)).json();

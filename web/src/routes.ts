import { Page } from "./types";
import Appointments from "./pages/Appointments";
import Dashboard from "./pages/Dashboard";
import FAQ from "./pages/FAQ";
import Medications from "./pages/Medications";
import Settings from "./pages/Settings";
import Schedules from "./pages/Schedules";
import Adherence from "./pages/Adherence";
import NewSchedule from "./pages/NewSchedule";
import NewMedication from "./pages/NewMedication";
import NewAppointment from "./pages/NewAppointment";
import EditMedication from "./pages/EditMedication";
import EditAppointment from "./pages/EditAppointment";
import EditSchedule from "./pages/EditSchedule";
import Assistant from "./pages/Assistant";


interface PageMap {
	[key: string]: Page
}

const pageMap: PageMap = {
	Dashboard: new Dashboard(),
	Assistant: new Assistant(),
	Medications: new Medications(),
	NewMedication: new NewMedication(),
	EditMedication: new EditMedication(),
	Appointments: new Appointments(),
	NewAppointment: new NewAppointment(),
	EditAppointment: new EditAppointment(),
	Schedules: new Schedules(),
	NewSchedule: new NewSchedule(),
	EditSchedule: new EditSchedule(),
	Adherence: new Adherence(),
	FAQ: new FAQ(),
	Settings: new Settings(),
}

export enum Pages {
	DASHBOARD = "Dashboard",
	ASSISTANT = "Assistant",
	MEDICATIONS = "Medications",
	NEW_MEDICATION = "NewMedication",
	EDIT_MEDICATION = "EditMedication",
	APPOINTMENTS = "Appointments",
	NEW_APPOINTMENT = "NewAppointment",
	EDIT_APPOINTMENT = "EditAppointment",
	SCHEDULES = "Schedules",
	NEW_SCHEDULE = "NewSchedule",
	EDIT_SCHEDULE = "EditSchedule",
	ADHERENCE = "Adherence",
	FAQ = "FAQ",
	SETTINGS = "Settings",
}

export default pageMap

export interface Page {
	render(props: PageProps): void
};

export type Component = <T>(props: Record<string, T>) => string;

export type ComposeElement = {
	parent: Element
	child: string
	position: "beforebegin" | "beforeend" | "afterbegin" | "afterend",
}

export type NextPageData = {
	detail: { [key: string]: any };
};

export type ComponentProps = {
	parent: Element,
	data: { [key: string]: any } | null
};

export type PageProps = {
	root: Element,
	nextPageData: NextPageData | null
};

export type BaseUserModel = {
	first_name: string,
	last_name: string,
	email: string,
	phone_number: string,
	user_type: string,
	gender: string,
	password: string
};

export type UserModel = { id: string } & BaseUserModel;

export type BaseAppointmentModel = {
	reason: string,
	location: string
};

export type AppointmentModel = { id: string } & BaseAppointmentModel;

export type BaseMedicationModel = {
	brand_name: string,
	generic_name: string | null,
	description: string,
	strength: string,
	dosage: number,
};

export type NewMedicationModel = {
	dosage_form_id: number,
	medication_route_id: number
} & BaseMedicationModel;

export type MedicationModel = {
	id: string,
	dosage_form: string,
	medication_route: string
} & BaseMedicationModel;

export type MedicationRouteModel = {
	id: string,
	name: string,
	friendly_name: string,
	description: string
};

export type DosageFormModel = {
	id: string,
	name: string,
	friendly_name: string,
	description: string
};

export type BaseScheduleModel = {
	begin_date: string,
	end_date: string | null,
	begin_time: string,
	end_time: string | null,
	schedule_type: string,
	repeated: string | null,
	repetition_step: number,
	repeated_monthly_on: string | null,
	repeated_until: string | null,
	repeated_until_date: string | null,
	repeated_reps: number | null,
};

export type NewScheduleModel = {
	medication_id: string | null,
	appointment_id: string | null,
} & BaseScheduleModel

export type ScheduleModel = {
	id: string
	medication: string | null,
	appointment: string | null,
} & BaseScheduleModel;


export type AdherenceModel = {
	datetime: string
	adherence_time: string | null,
	adherence_status: string | null,
	reminder_status: string | null,
	non_adherence_reason: string | null,
	notes: string | null,
	schedule_id: string,
	repeated: string | null,
	repetition_step: number
	repeated_monthly_on: string | null
	rep_count: number
};

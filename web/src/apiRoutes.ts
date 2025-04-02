const BASE_URL = "http://0.0.0.0:8000"

export default {
	ADD_MEDICATION: `${BASE_URL}/medications/new`,
	ADD_APPOINTMENT: `${BASE_URL}/appointments/new`,
	ADD_SCHEDULE: `${BASE_URL}/schedules/new`,
	GET_MEDICATIONS: `${BASE_URL}/medications/all`,
	GET_MEDICATION_ROUTES: `${BASE_URL}/medications/routes`,
	GET_DOSAGE_FORMS: `${BASE_URL}/medications/forms`,
	GET_SCHEDULES: `${BASE_URL}/schedules/all`,
	GET_APPOINTMENTS: `${BASE_URL}/appointments/all`,
	GET_ADHERENCE_DATA: `${BASE_URL}/adherence/all`,
	TALK_ASSISTANT: `${BASE_URL}/assistant/talk`
}

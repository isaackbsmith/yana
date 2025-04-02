from yana.assistant.paths.log_intake import log_intake
from yana.assistant.paths.add_medical_appointment import add_medical_appointment
from yana.assistant.paths.add_medication import add_medication
from yana.assistant.paths.cancel_reminder import cancel_reminder
from yana.assistant.paths.check_history import check_history
from yana.assistant.paths.check_schedule import check_schedule
from yana.assistant.paths.daily_health_check import daily_health_check
from yana.assistant.paths.get_adherence_summary import get_adherence_summary
from yana.assistant.paths.get_medical_appointment_info import get_medical_appointment_info
from yana.assistant.paths.get_medication_info import get_medication_info
from yana.assistant.paths.modify_reminder import modify_reminder
from yana.assistant.paths.remove_medical_appointment import remove_medical_appointment
from yana.assistant.paths.remove_medication import remove_medication
from yana.assistant.paths.set_reminder import set_reminder
from yana.assistant.paths.symptoms_check import symptoms_check
from yana.assistant.paths.update_dosage import update_dosage
from yana.assistant.paths.update_medical_appointment import update_medical_appointment
from yana.assistant.paths.general_interaction_path import general_interaction_path
from yana.domain.intents import Intent
from yana.domain.types import ConversationPath


interaction_path_map: dict[Intent, ConversationPath] = {
    Intent.CHECK_SCHEDULE: check_schedule,
    # Intent.SET_REMINDER: set_reminder,
    # Intent.MODIFY_REMINDER: modify_reminder,
    # Intent.CANCEL_REMINDER: cancel_reminder,
    # Intent.ADD_MEDICATION: add_medication,
    # Intent.REMOVE_MEDICATION: remove_medication,
    # Intent.UPDATE_DOSAGE: update_dosage,
    Intent.GET_MEDICATION_INFO: get_medication_info,
    # Intent.ADD_MEDICAL_APPOINTMENT: add_medical_appointment,
    # Intent.REMOVE_MEDICAL_APPOINTMENT: remove_medical_appointment,
    # Intent.GET_MEDICAL_APPOINTMENT_INFO: get_medical_appointment_info,
    # Intent.UPDATE_MEDICAL_APPOINTMENT: update_medical_appointment,
    # Intent.DAILY_HEALTH_CHECK: daily_health_check,
    # Intent.SYMPTOMS_CHECK: symptoms_check,
    Intent.GET_ADHERENCE_SUMMARY: get_adherence_summary,
    # Intent.CHECK_HISTORY: check_history,
    Intent.LOG_INTAKE: log_intake
}

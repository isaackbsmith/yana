from enum import Enum
from typing import Self


class Intent(str, Enum):
    CHECK_SCHEDULE = "Check_Schedule"
    LOG_INTAKE = "Log_Intake"
    SKIP_DOSE = "Skip_Dose"
    SET_REMINDER = "Set_Reminder"
    MODIFY_REMINDER = "Modify_Reminder"
    CANCEL_REMINDER = "Cancel_Reminder"
    ADD_MEDICATION = "Add_Medication"
    REMOVE_MEDICATION = "Remove_Medication"
    UPDATE_DOSAGE = "Update_Dosage"
    GET_MEDICATION_INFO = "Get_Medication_Info"
    ASK_SIDE_EFFECTS = "Ask_Side_Effects"
    MEDICATION_INTERACTIONS = "Medication_Interactions"
    REQUEST_REFILL = "Request_Refill"
    ADD_MEDICAL_APPOINTMENT = "Add_Medical_Appointment"
    REMOVE_MEDICAL_APPOINTMENT = "Remove_Medical_Appointment"
    GET_MEDICAL_APPOINTMENT_INFO = "Get_Medical_Appointment_Info"
    UPDATE_MEDICAL_APPOINTMENT = "Update_Medical_Appointment"
    GET_NEXT_APPOINTMENT_REMINDER = "Get_Next_Appointment_Reminder"
    EMERGENCY_ASSISTANCE = "Emergency_Assistance"
    FIRST_AID_INFO = "First_Aid_Info"
    EMERGENCY_CONTACT = "Emergency_Contact"
    DAILY_HEALTH_CHECK = "Daily_Health_Check"
    GENERAL_SMALL_TALK = "General_Small_Talk"
    HEALTHY_LIFESTYLE_TIPS = "Healthy_Lifestyle_Tips"
    SYMPTOMS_CHECK = "Symptoms_Check"
    LOCATE_NEAREST_PHARMACY = "Locate_Nearest_Pharmacy"
    PROVIDE_FEEDBACK = "Provide_Feedback"
    GET_ADHERENCE_SUMMARY = "Get_Adherence_Summary"
    GENERAL_WELLBEING_CHECK = "General_Wellbeing_Check"
    CHECK_HISTORY = "Check_History"

    @classmethod
    def try_from_str(cls: type[Self], value: str) -> Self:
        for intent in cls:
            if intent.value == value:
                return intent
        raise ValueError(f"{value} must be a valid intent")

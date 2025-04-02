from enum import Enum
from typing import Self
from yana.utils.getters import (
    get_user_name,
    get_user_title,
    get_time,
    get_medication,
    get_emergency_number,
    get_condition,
    get_dosage,
    get_date,
    get_value,
    get_doctor_name,
    get_mood,
    get_side_effect,
    get_contact_name,
    get_contact_number,
    get_location,
)


class Placeholder(str, Enum):
    USER_NAME = "user_name"
    USER_TITLE = "user_title"
    TIME = "time"
    MEDICATION = "medication"
    EMERGENCY_NUMBER = "emergency_number"
    CONDITION = "condition"
    DOSAGE = "dosage"
    SIDE_EFFECT = "side_effect"
    CONTACT_NAME = "contact_name"
    CONTACT_NUMBER = "contact_number"
    VALUE = "value"
    MOOD = "mood"
    DOCTOR_NAME = "doctor_name"
    DATE = "date"
    LOCATION = "location"

    @classmethod
    def try_from_str(cls: type[Self], value: str) -> Self:
        for placeholder in cls:
            if placeholder.value == value.lower():
                return placeholder
        raise ValueError(f"{value} must be a valid placeholder")


placeholder_map = {
    Placeholder.USER_NAME: get_user_name,
    Placeholder.USER_TITLE: get_user_title,
    Placeholder.TIME: get_time,
    Placeholder.MEDICATION: get_medication,
    Placeholder.EMERGENCY_NUMBER: get_emergency_number,
    Placeholder.CONDITION: get_condition,
    Placeholder.DOSAGE: get_dosage,
    Placeholder.SIDE_EFFECT: get_side_effect,
    Placeholder.CONTACT_NAME: get_contact_name,
    Placeholder.CONTACT_NUMBER: get_contact_number,
    Placeholder.VALUE: get_value,
    Placeholder.MOOD: get_mood,
    Placeholder.DOCTOR_NAME: get_doctor_name,
    Placeholder.DATE: get_date,
    Placeholder.LOCATION: get_location,
}

from enum import Enum
from typing import Self


class NamedEntity(str, Enum):
    ACTIVITY = "Activity"
    ADMINISTRATION = "Administration"
    AGE = "Age"
    AREA = "Area"
    BIOLOGICAL_ATTRIBUTE = "Biological_attribute"
    BIOLOGICAL_STRUCTURE = "Biological_structure"
    CLINICAL_EVENT = "Clinical_event"
    COLOR = "Color"
    COREFERENCE = "Coreference"
    DATE = "Date"
    DETAILED_DESCRIPTION = "Detailed_description"
    DIAGNOSTIC_PROCEDURE = "Diagnostic_procedure"
    DISEASE_DISORDER = "Disease_disorder"
    DISTANCE = "Distance"
    DOSAGE = "Dosage"
    DURATION = "Duration"
    FAMILY_HISTORY = "Family_history"
    FREQUENCY = "Frequency"
    HEIGHT = "Height"
    HISTORY = "History"
    LAB_VALUE = "Lab_value"
    MASS = "Mass"
    MEDICATION = "Medication"
    NON_BIOLOGICAL_DETAILED_DESCRIPTION = "Non[biological](Detailed_description"
    NONBIOLOGICAL_LOCATION = "Nonbiological_location"
    OCCUPATION = "Occupation"
    OTHER_ENTITY = "Other_entity"
    OTHER_EVENT = "Other_event"
    OUTCOME = "Outcome"
    PERSONAL_BIOLOGICAL_STRUCTURE = "Personal_[back](Biological_structure"
    PERSONAL_BACKGROUND = "Personal_background"
    QUALITATIVE_CONCEPT = "Qualitative_concept"
    QUANTITATIVE_CONCEPT = "Quantitative_concept"
    SEVERITY = "Severity"
    SEX = "Sex"
    SHAPE = "Shape"
    SIGN_SYMPTOM = "Sign_symptom"
    SUBJECT = "Subject"
    TEXTURE = "Texture"
    THERAPEUTIC_PROCEDURE = "Therapeutic_procedure"
    TIME = "Time"
    VOLUME = "Volume"
    WEIGHT = "Weight"

    @classmethod
    def try_from_str(cls: type[Self], value: str) -> Self:
        for entity in cls:
            if entity.value == value:
                return entity
        raise ValueError(f"{value} must be a valid entity")

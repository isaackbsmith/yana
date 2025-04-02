from yana.domain.entities import NamedEntity
from yana.domain.intents import Intent
from yana.domain.models.medication import BaseMedicationModel
from yana.domain.types import NamedEntities, YANAConfig
from yana.utils.conversation import get_entity


async def add_medication(config: YANAConfig, intent: Intent, entities: NamedEntities) -> None:

    medication = get_entity(config, "medication", NamedEntity.MEDICATION, None)

    # If the recognized medication is 'medication' or other variants,
    # ask again
    if medication in ["medication", "medicine"]:
        medication = get_entity(config, "medication", NamedEntity.MEDICATION, None)

    dosage = get_entity(config, "dosage", NamedEntity.DOSAGE, None) 
    time = get_entity(config, "time", NamedEntity.TIME, entities)
    date = get_entity(config, "date", NamedEntity.DATE, entities) 
    duration = get_entity(config, "duration", NamedEntity.DURATION, entities) 
    lab_value = get_entity(config, "lab_value", NamedEntity.LAB_VALUE, entities)
    frequency = get_entity(config, "frequency", NamedEntity.FREQUENCY, entities) 

    print(f"After processing ==> Medication: {medication} and Dosage: {dosage}")

    # Ask the user for the dosage form and route

    new_medication = BaseMedicationModel(
        generic_name="",
        brand_name=medication,
        description="",
        dosage=dosage,
        dosage_form_id=1,
        medication_route_id=1
    )


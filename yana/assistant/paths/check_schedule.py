from yana.domain.intents import Intent
from yana.domain.models.assistant import AudioResponseSchema
from yana.domain.types import NamedEntities, YANAConfig
from yana.lib.speech_synthesizer import SPEECH_SYNTHESIZER
from yana.service.adherence import fetch_next_adherence_slot
from yana.service.schedules import fetch_schedule_appointment, fetch_schedule_medication


async def check_schedule(config: YANAConfig, intent: Intent, entities: NamedEntities, web: bool) -> AudioResponseSchema | None:
    # See if there's a medication, appointment, date or time
    next_slot = await fetch_next_adherence_slot(config)
    print("SLOT HERE: ====> ", next_slot)

    if not next_slot:
        if web:
            return SPEECH_SYNTHESIZER.respond_web("You do not have any upcoming medications or appointments")
        SPEECH_SYNTHESIZER.speak(["You do not have any upcoming medications or appointments"])
        SPEECH_SYNTHESIZER.speak(["Would you like to set a schedule"])
        return

    medication = await fetch_schedule_medication(config, next_slot.schedule_id)
    appointment = await fetch_schedule_appointment(config, next_slot.schedule_id)
    time = f"is at {next_slot.datetime.to_datetime_string()}"

    print("MEDICATION HERE: ====> ", medication)
    print("APPOINTMENT HERE: ====> ", appointment)
    if medication:
        if web:
            return SPEECH_SYNTHESIZER.respond_web(f"Your next medication is {medication.brand_name}...{time}")
        SPEECH_SYNTHESIZER.speak([f"Your next medication is {medication.brand_name}", time])
        return

    if appointment:
        if web:
            return SPEECH_SYNTHESIZER.respond_web(f"Your next appointment is {appointment.reason} {time}")
        SPEECH_SYNTHESIZER.speak([f"Your next appointment is {appointment.reason}", time])
        return



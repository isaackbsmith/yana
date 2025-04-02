from yana.domain.intents import Intent
from yana.domain.models.adherence import AdherenceStatus, ReminderStatus
from yana.domain.models.assistant import AudioResponseSchema
from yana.domain.types import NamedEntities, YANAConfig
from yana.lib.speech_synthesizer import SPEECH_SYNTHESIZER
from yana.service.adherence import fetch_slot_by_reminder_status, set_adherence_status


async def log_intake(config: YANAConfig, intent: Intent, entities: NamedEntities, web: bool) -> AudioResponseSchema | None:


    slot = await fetch_slot_by_reminder_status(config, ReminderStatus.SENT)

    if slot:
        await set_adherence_status(config, slot, AdherenceStatus.FULLY_ADHERENT)
        if web:
            return SPEECH_SYNTHESIZER.respond_web("That is great... I will update the database accordingly... keep it up")

        SPEECH_SYNTHESIZER.speak(["That is great... I will update the database accordingly... keep it up"])
    else:
        SPEECH_SYNTHESIZER.speak(["It looks like you don't have to take any medication now..."])


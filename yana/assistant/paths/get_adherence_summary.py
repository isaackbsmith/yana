from pathlib import Path
from yana.domain.intents import Intent
from yana.domain.models.assistant import AudioResponseSchema
from yana.domain.types import NamedEntities, YANAConfig
from yana.lib.speech_synthesizer import SPEECH_SYNTHESIZER
from yana.service.adherence import fetch_adherence_rate


async def get_adherence_summary(config: YANAConfig, intent: Intent, entities: NamedEntities, web: bool) -> AudioResponseSchema | None:
    overall_adherence_rate = await fetch_adherence_rate(config)

    if not overall_adherence_rate:
        if web:
            return SPEECH_SYNTHESIZER.respond_web("There's not enough data to generate a summary for you at this time")

        SPEECH_SYNTHESIZER.speak(["There's not enough data to generate a summary for you at this time"])
        return

    if web:
        response = f"""
        Sumary of your adherence rate...Out of {str(overall_adherence_rate.total_slots)} total slots
        {str(overall_adherence_rate.fully_adherent_count)} were fully adherent...
        resulting in a {str(overall_adherence_rate.adherence_rate)} percent adherence rate...
        Keep it up
        """
        return SPEECH_SYNTHESIZER.respond_web(response)


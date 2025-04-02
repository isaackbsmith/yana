import asyncio
from yana.domain.models.adherence import ReminderStatus
from yana.domain.types import YANAConfig
from yana.lib.speech_synthesizer import SpeechSynthesizer
from yana.service.reminder import fetch_due_schedule, set_reminder_status
from yana.service.schedules import fetch_schedule_medication
from yana.utils.config import get_config
from yana.domain.logger import reminder_logger


async def check_and_remind_due_schedule(config: YANAConfig, tts: SpeechSynthesizer):
    """Gets due schedule and notifies user"""
    reminder_logger.info("Checking due schedules")
    slot = await fetch_due_schedule(config)
    print("SLOT", slot)

    if slot:
        medication = await fetch_schedule_medication(config, slot.schedule_id)
        print("MEDICATION", medication)
        if medication:
            reminder_logger.info(f"Schedule: {medication.brand_name} is due now at {slot.datetime.to_day_datetime_string()}")
            tts.speak(["Hello, it is time to take your medication..."])
            await asyncio.sleep(1)
            tts.speak([f"You need to take the {medication.brand_name} drug..."])
            await set_reminder_status(config, slot, ReminderStatus.SENT)
            await asyncio.sleep(2)
            tts.speak(["Let me know when you take your medication..."])
    reminder_logger.info("Done checking due schedules")



async def main():
    config = get_config()
    tts = SpeechSynthesizer(config)
    while True:
        await asyncio.create_task(check_and_remind_due_schedule(config, tts))
        await asyncio.sleep(3)

if __name__ == "__main__":
    asyncio.run(main())


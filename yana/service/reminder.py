import uuid

import pendulum

from yana.data.queries.adherence import (
    insert_adherence_slot,
    update_reminder_status,
)
from yana.data.queries.reminder import select_due_schedule
from yana.data.schemas.adherence import NewAdherenceSlotSchema
from yana.domain.models.adherence import FullAdherenceSlotModel, ReminderStatus
from yana.domain.models.schedule import RepeatedUntil
from yana.domain.types import YANAConfig
from yana.service.schedules import fetch_schedule
from yana.utils.adherence import get_next_slot_delta, should_create_slot


async def fetch_due_schedule(config: YANAConfig) -> FullAdherenceSlotModel | None:
    current_datetime = pendulum.now()
    result = await select_due_schedule(config, current_datetime.int_timestamp)
    if result and isinstance(result, list) and len(result) > 0:
        slots = list(
            map(lambda x: FullAdherenceSlotModel(**x.model_dump()), result)
        )
        # Get the most due
        for slot in slots:
            # Return slot if it falls on the same day
            print(f"{slot.datetime} <==============> {current_datetime}")
            if (slot.datetime.day == current_datetime.day) and (slot.datetime <= current_datetime):
                return slot
    return


async def create_next_adherence_slot(config: YANAConfig, current_slot: FullAdherenceSlotModel):
    """
    Create adherence slots for a given schedule

    arguments:
        schedule: The schedule model
    """

    # Get the original schedule
    schedule = await fetch_schedule(config, current_slot.schedule_id)

    if not schedule:
        return

    # Check if next slot is within schedule
    if schedule.end_date:
        if current_slot.datetime.date() > schedule.end_date.date():
            return

    # Check if rep_count is within n_repetitions
    if schedule.repeated_until is RepeatedUntil.N_REPETITIONS:
        if schedule.repeated_reps and schedule.repeated_reps <= current_slot.rep_count:
            return

    # Get the duration offset for the next slot
    current_date = current_slot.datetime + get_next_slot_delta(current_slot)

    # Generate individual event slots based on the schedule's recurrence
    # pattern and other parameters.
    if should_create_slot(current_slot, current_date):
        id = str(uuid.uuid4())
        slot = NewAdherenceSlotSchema(
            id=id,
            datetime=current_date.int_timestamp,
            schedule_id=current_slot.schedule_id
        )
        await insert_adherence_slot(config, slot)


async def set_reminder_status(config: YANAConfig, slot: FullAdherenceSlotModel, status: ReminderStatus) -> None:
    await update_reminder_status(config, slot.id, status.value)

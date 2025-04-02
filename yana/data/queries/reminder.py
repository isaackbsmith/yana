from yana.data.database import run_query
from yana.data.schemas.adherence import FullAdherenceSlotSchema
from yana.domain.exceptions import DatabaseError, QueryError
from yana.domain.types import YANAConfig


async def select_due_schedule(config: YANAConfig, current_date: int):
    sql = """
        SELECT
            slot.id,
            slot.datetime,
            slot.adherence_time,
            slot.adherence_status,
            slot.reminder_status,
            slot.non_adherence_reason,
            slot.notes,
            slot.rep_count,
            slot.schedule_id,
            sched.repeated,
            sched.repetition_step,
            sched.repeated_monthly_on
        FROM adherence_slots AS slot
        INNER JOIN schedules AS sched ON slot.schedule_id = sched.id
        WHERE slot.datetime <= :current_date AND slot.reminder_status IS NULL
    """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"current_date": current_date},
            factory=FullAdherenceSlotSchema,
            pragma="all",
        )
    except DatabaseError:
        raise QueryError("Error selecting adherence slot")

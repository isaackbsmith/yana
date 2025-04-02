from yana.data.database import run_query
from yana.data.schemas.adherence import AdherenceRateSchema, AdherenceSlotSchema, FullAdherenceSlotSchema, NewAdherenceSlotSchema
from yana.domain.exceptions import DatabaseError, QueryError
from yana.domain.types import YANAConfig


async def select_adherence_slot(config: YANAConfig, id: str):
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
        WHERE id = :id
    """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"id": id},
            factory=AdherenceSlotSchema,
            pragma="one",
        )
    except DatabaseError:
        raise QueryError("Error selecting adherence slot")


async def select_adherence_schedule_slot(config: YANAConfig, schedule_id: str):
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
        WHERE schedule_id = :schedule_id
    """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"schedule_id": schedule_id},
            factory=FullAdherenceSlotSchema,
            pragma="many",
            limit=10
        )
    except DatabaseError:
        raise QueryError("Error selecting adherence slots")

async def select_all_adherence_slots(config: YANAConfig):
    sql = """
        SELECT
            id,
            datetime,
            adherence_time,
            adherence_status,
            reminder_status,
            non_adherence_reason,
            notes,
            rep_count,
            schedule_id
        FROM adherence_slots
        ORDER BY datetime
    """
    try:
        return await run_query(
            config=config,
            sql=sql,
            factory=AdherenceSlotSchema,
            pragma="all",
        )
    except DatabaseError:
        raise QueryError("Error selecting adherence slots")


async def select_next_adherence_slot(config: YANAConfig, current_date: int):
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
        WHERE slot.datetime >= :current_date
        ORDER BY slot.datetime
    """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"current_date": current_date},
            factory=FullAdherenceSlotSchema,
            pragma="one",
        )
    except DatabaseError:
        raise QueryError("Error selecting adherence slot")


async def select_slot_by_reminder_status(config: YANAConfig, current_date: int, status: str):
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
        WHERE slot.datetime <= :current_date AND slot.reminder_status = :status
        ORDER BY slot.datetime DESC;
    """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"current_date": current_date, "status": status},
            factory=FullAdherenceSlotSchema,
            pragma="one",
        )
    except DatabaseError:
        raise QueryError("Error selecting adherence slot")


async def select_adherence_history(config: YANAConfig, date_range: dict[str, int]):
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
        WHERE slot.datetime BETWEEN :begin AND :end;
    """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params=date_range,
            factory=FullAdherenceSlotSchema,
            pragma="all",
        )
    except DatabaseError:
        raise QueryError("Error selecting adherence slot")


async def insert_adherence_slot(config: YANAConfig, slot: NewAdherenceSlotSchema):
    sql = """
        INSERT INTO adherence_slots (
            id,
            datetime,
            schedule_id
        ) VALUES (
            :id,
            :datetime,
            :schedule_id
        );
        """
    try:
        return await run_query(
            config=config, sql=sql, params=slot.model_dump(), factory=AdherenceSlotSchema
        )
    except DatabaseError:
        raise QueryError("Error inserting new adherence slot")


async def update_adherence_slot(config: YANAConfig, slot: FullAdherenceSlotSchema):
    sql = """
        UPDATE adherence_slots
        SET
            non_adherece_reason = :non_adherence_reason,
            notes = :notes
        WHERE id = :id;
        """
    try:
        return await run_query(
            config=config, sql=sql, params=slot.model_dump(), factory=FullAdherenceSlotSchema
        )
    except DatabaseError:
        raise QueryError("Error updating adherence slot")


async def update_adherence_status(config: YANAConfig, slot_id: str, status: str):
    sql = """
        UPDATE adherence_slots
        SET
            adherence_status = :adherence_status
        WHERE id = :slot_id;
        """
    try:
        return await run_query(
            config=config, sql=sql,
            params={"slot_id": slot_id, "adherence_status": status},
            factory=FullAdherenceSlotSchema
        )
    except DatabaseError:
        raise QueryError("Error updating adherence status")


async def update_reminder_status(config: YANAConfig, slot_id: str, status: str):
    sql = """
        UPDATE adherence_slots
        SET
            reminder_status = :reminder_status
        WHERE id = :slot_id;
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"slot_id": slot_id, "reminder_status": status},
            factory=FullAdherenceSlotSchema
        )
    except DatabaseError:
        raise QueryError("Error updating reminder status")


async def delete_adherence_slot(config: YANAConfig, id: str):
    sql = """
        DELETE FROM adherence_slots WHERE id = :id;
        """
    try:
        return await run_query(
            config=config,
            sql=sql,
            params={"id": id},
            factory=NewAdherenceSlotSchema
        )
    except DatabaseError:
        raise QueryError("Error deleting adherence slot")


# Stats
async def select_overall_adherence_rate(config: YANAConfig):
    sql = """
    SELECT 
        COUNT(*) AS total_slots,
        SUM(CASE WHEN adherence_status = 'fully_adherent' THEN 1 ELSE 0 END) AS fully_adherent_count,
        ROUND(SUM(CASE WHEN adherence_status = 'fully_adherent' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS adherence_rate
    FROM adherence_slots
    WHERE adherence_status IS NOT NULL;
    """
    try:
        return await run_query(
            config=config,
            sql=sql,
            factory=AdherenceRateSchema
        )
    except DatabaseError:
        raise QueryError("Error deleting adherence slot")

from yana.data.schemas.schedule import ScheduleSchema
from yana.domain.models.schedule import Repeated, RepeatedMonthlyOn, RepeatedUntil, ScheduleModel
from yana.utils.datetime import date_from_ts, time_from_secs, to_unix_date_ts, to_unix_time_ts


def to_schedule_model(schedule: ScheduleSchema) -> ScheduleModel:
    model = ScheduleModel(
        id=schedule.id,
        begin_date=date_from_ts(schedule.begin_date),
        end_date=date_from_ts(schedule.end_date) if schedule.end_date else None,
        begin_time=time_from_secs(schedule.begin_time),
        end_time=time_from_secs(schedule.end_time) if schedule.end_time else None,
        schedule_type=schedule.schedule_type,
        repeated=Repeated.try_from_str(schedule.repeated)
        if schedule.repeated
        else None,
        repetition_step=schedule.repetition_step,
        repeated_monthly_on=RepeatedMonthlyOn.try_from_str(
            schedule.repeated_monthly_on
        )
        if schedule.repeated_monthly_on
        else None,
        repeated_until=RepeatedUntil.try_from_str(schedule.repeated_until)
        if schedule.repeated_until
        else None,
        repeated_until_date=date_from_ts(schedule.repeated_until_date)
        if schedule.repeated_until_date
        else None,
        repeated_reps=schedule.repeated_reps,
        medication_id=schedule.medication_id,
        appointment_id=schedule.appointment_id,
    )
    return model

def to_schedule_schema(schedule: ScheduleModel, id: str) -> ScheduleSchema:
    schema = ScheduleSchema(
        id=id,
        begin_date=to_unix_date_ts(schedule.begin_date),
        end_date=to_unix_date_ts(schedule.end_date) if schedule.end_date else None,
        begin_time=to_unix_time_ts(schedule.begin_time),
        end_time=to_unix_time_ts(schedule.end_time) if schedule.end_time else None,
        schedule_type=schedule.schedule_type,
        repeated=schedule.repeated.value if schedule.repeated else None,
        repetition_step=schedule.repetition_step,
        repeated_monthly_on=schedule.repeated_monthly_on.value
        if schedule.repeated_monthly_on
        else None,
        repeated_until=schedule.repeated_until.value
        if schedule.repeated_until
        else None,
        repeated_until_date=schedule.repeated_until_date.int_timestamp
        if schedule.repeated_until_date
        else None,
        repeated_reps=schedule.repeated_reps,
        medication_id=schedule.medication_id,
        appointment_id=schedule.appointment_id,
    )
    return schema

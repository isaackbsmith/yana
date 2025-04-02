import pendulum
from pendulum import DateTime, Duration
from yana.domain.models.adherence import FullAdherenceSlotModel
from yana.domain.models.schedule import Repeated, RepeatedMonthlyOn


def should_create_slot(slot: FullAdherenceSlotModel, current_date: DateTime):
    """
    Determine if a slot should be created for the given date based on the schedule's recurrence pattern

    arguments:
        schedule: The schedule model
        current_date: the date to check

    returns:
        bool: True if a slot should be created, False otherwise
    """

    match slot.repeated:
        case Repeated.MINUTELY | Repeated.HOURLY | Repeated.ANNUALLY:
            return True
        case Repeated.WEEKLY:
            # Check if the current day of the week matches the schedule's start day
            # Check for the day of the week too
            return current_date.weekday() == slot.date.weekday()
        case Repeated.MONTHLY:
            match slot.repeated_monthly_on:
                case RepeatedMonthlyOn.SAME_DAY:
                    # Check if it's the same day of the month
                    return current_date.day == slot.date.day
                case RepeatedMonthlyOn.SAME_WEEKDAY:
                    # Check if it's the same weekday and week of the month
                    return (current_date.weekday() == slot.date.weekday() and (current_date.day - 1) // 7 == (slot.date.day - 1) // 7)
        case _:
            return False


def get_next_slot_delta(slot: FullAdherenceSlotModel) -> Duration:
    """
    Calculate the time delta to the next slot based on the schedule's recurrence pattern.

    arguments:
        schedule: The schedule model

    returns:
        Duration: The time difference to the next slot
    """
    match slot.repeated:
        case Repeated.MINUTELY:
            return pendulum.duration(minutes=slot.repetition_step)
        case Repeated.HOURLY:
            return pendulum.duration(hours=slot.repetition_step)
        case Repeated.DAILY:
            return pendulum.duration(days=slot.repetition_step)
        case Repeated.WEEKLY:
            return pendulum.duration(weeks=slot.repetition_step)
        case Repeated.MONTHLY:
            return pendulum.duration(months=slot.repetition_step)
        case Repeated.ANNUALLY:
            return pendulum.duration(years=slot.repetition_step)
        case _:
            return pendulum.duration(days=0)

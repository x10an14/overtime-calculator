"""Module containing majory of calulation functions and their helpers."""
from datetime import datetime
from datetime import timedelta
from collections import defaultdict

from . import default_parse_fmt
from . import log_function_entry_and_exit


@log_function_entry_and_exit
def parse_row(row, field_names, datetime_parse_fmt=default_parse_fmt, has_duration=True):
    # TODO: ADD DOCSTRING

    # TODO: figure out which fields (if any) have datetime

    # TODO: Replace these hardcoded field_names with names decided upon
    #       through above todo.

    # Get date of current event/row
    start_time = row[field_names[0]]
    start_time = datetime.strptime(start_time, datetime_parse_fmt)
    duration = row[field_names[1]]

    if not has_duration:
        # Get stop time to calculate duration
        stop_time = datetime.strptime(duration, datetime_parse_fmt)

        # Get duration as "HH:MM":
        minutes = int((stop_time - start_time).total_seconds() // 60)
        hours = str(minutes // 60).zfill(2)
        minutes = str(minutes % 60).zfill(2)

        duration = ":".join((hours, minutes))

    return (duration, start_time.isocalendar())


@log_function_entry_and_exit
def parse_csv_reader_content(input_data, **kwargs):
    # TODO: ADD DOCSTRING

    total_sum, aggregate_records = timedelta(0), defaultdict(dict)
    for row in input_data:
        (duration, (_, week_nr, week_day)) = parse_row(row, **kwargs)

        t = datetime.strptime(duration, "%H:%M")
        total_sum += timedelta(hours=t.hour, minutes=t.minute)

        if week_nr not in aggregate_records:
            aggregate_records[week_nr] = defaultdict(list)

        if week_day not in aggregate_records[week_nr]:
            aggregate_records[week_nr][week_day] = [duration]
        else:
            aggregate_records[week_nr][week_day].append(duration)

    # add total amount of seconds to return object
    aggregate_records["total_sum"] = int(total_sum.total_seconds())

    return aggregate_records


@log_function_entry_and_exit
def parse_aggregate_weeks_and_weekdays(aggregate_data, hours_per_week=37.5):
    # TODO: ADD DOCSTRING

    def get_timedelta_from_str(input_str, parse_fmt="%H:%M"):
        t = datetime.strptime(input_str, parse_fmt)
        return timedelta(hours=t.hour, minutes=t.minute)

    total_balance, hours_per_week = timedelta(0), timedelta(hours=hours_per_week)
    for week, days in aggregate_data.items():
        if week == "total_sum":
            continue

        week_sum = timedelta(0)
        for day, records in days.items():
            week_sum += sum(
                get_timedelta_from_str(record)
                for record in records
            )
        week_balance = week_sum - hours_per_week

        aggregate_data[week]["sum"] = int(week_sum.total_seconds())
        aggregate_data[week]["balance"] = int(week_balance.total_seconds())
        total_balance += week_balance

    total_balance = aggregate_data["total_sum"] - int(total_balance.total_seconds())
    aggregate_data["hours_per_week"] = hours_per_week.total_seconds() / 3600
    aggregate_data["total_balance"] = total_balance
    return aggregate_data

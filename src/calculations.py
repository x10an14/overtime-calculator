"""Module containing majory of calulation functions and their helpers."""
from datetime import datetime
from datetime import timedelta
import logging

from . import default_parse_fmt
from . import default_work_days
from . import default_work_hours_in_week
from . import log_function_entry_and_exit


# @log_function_entry_and_exit
def parse_row(row, datetime_parse_fmt=default_parse_fmt):
    # TODO: ADD DOCSTRING

    # TODO: figure out which fields (if any) have datetime

    # TODO: Replace these hardcoded field_names with names decided upon
    #       through above todo.
    start_field_name, stop_field_name = "First Check-In", "Last Check-Out"
    start_time = datetime.strptime(row[start_field_name], default_parse_fmt)
    stop_time = datetime.strptime(row[stop_field_name], default_parse_fmt)

    duration = (stop_time - start_time)
    return (duration, start_time.isocalendar())


@log_function_entry_and_exit
def parse_csv_reader_content(csv_reader, work_days=default_work_days):
    # TODO: ADD DOCSTRING
    def help_func(nested_obj, first_key, second_key, new_val):
        try:
            nested_obj[first_key][second_key].append(new_val)
        except KeyError as e:
            if e.args[0] == first_key:
                # if it's the first time we visit this week
                nested_obj[first_key] = dict()
                nested_obj[first_key][second_key] = [new_val]
            if e.args[0] == second_key:
                # If it's the first day we visit this day of this week
                nested_obj[first_key][second_key] = [new_val]

    total_sum = timedelta(0)
    aggregate_records, overtime_records = dict(), dict()
    for row in csv_reader:
        (duration, (_, week_nr, week_day)) = parse_row(row)
        total_sum += duration

        if week_day not in work_days.values():
            help_func(
                nested_obj=overtime_records,
                first_key=week_nr,
                second_key=week_day,
                new_val=duration)
        else:
            help_func(
                nested_obj=aggregate_records,
                first_key=week_nr,
                second_key=week_day,
                new_val=duration)

    # add total sum to return object
    aggregate_records["total_sum"] = total_sum

    return aggregate_records, overtime_records


@log_function_entry_and_exit
def parse_aggregate_weeks_and_weekdays(aggregate_data, hours_per_week=default_work_hours_in_week):
    # TODO: ADD DOCSTRING
    total_balance = timedelta(0)
    for week, days in aggregate_data.items():
        if week == "total_sum":
            continue
        week_sum = timedelta(0)
        for day, records in days.items():
            if day == "balance":
                continue
            for record in records:
                week_sum += record
        week_balance = hours_per_week - week_sum
        aggregate_data[week]["balance"] = week_balance
        total_balance += week_balance

    total_balance = aggregate_data["total_sum"] - total_balance
    aggregate_data["total_balance"] = total_balance
    return aggregate_data

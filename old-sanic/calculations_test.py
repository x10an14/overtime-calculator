from os import path as op

# PIP import(s):
import pytest

# Module import(s):
from src.file_manip import get_csv_file_content_as_dicts
from src.calculations import parse_row
from src.calculations import parse_csv_reader_content
from src.calculations import parse_aggregate_weeks_and_weekdays


CSV_FILES_FOLDER = op.join("tests", "data")


@pytest.mark.parametrize(
    "file_name,field_names,parse_fmt,has_duration,expected",
    [
        ("header_and_one_row_1.csv",
            ["First Check-In", "Last Check-Out"], "%d-%m-%Y %H:%M:%S", False,
            [
                ("00:00", (2016, 48, 1)),
                ("07:00", (2016, 35, 3)),
                ("06:40", (2016, 40, 5)),
                ("08:05", (2016, 40, 4)),
                ("07:30", (2016, 40, 2)), ]),
        ("header_and_one_row_2.csv",
            ["Date", "Duration"], "%d.%m.%Y", True,
            [
                ("06:30", (2016, 30, 1)), ]),
    ])
def test_valid_parse_row(file_name, field_names, parse_fmt, has_duration, expected):
    with open(op.join(CSV_FILES_FOLDER, file_name), "r") as f:
        return_dicts = get_csv_file_content_as_dicts(
            content=f.read(), file_name=file_name)

    rows = [parse_row(x, field_names, parse_fmt, has_duration) for x in return_dicts]

    # compare expected with returned:
    for x in expected:
        # Make sure all in expected are present in rows
        assert x in rows

    # compare returned with expected
    for x in rows:
        # Make sure all in rows are present in expected
        assert x in expected


@pytest.mark.parametrize(
    "input_data,expected,kwargs",
    [
        (
            [
                # input_data
                {
                    "Start time": "27-11-2016",
                    "End time": "28-11-2016",
                    "Hours": "0.00",
                    "Income": "0.00",
                    "First Check-In": "28-11-2016 08:20:00",
                    "Last Check-Out": "28-11-2016 08:20:00",
                },
                {
                    "Start time": "31-08-2016",
                    "End time": "01-09-2016",
                    "Hours": "7.00",
                    "Income": "0.00",
                    "First Check-In": "31-08-2016 10:00:00",
                    "Last Check-Out": "31-08-2016 17:00:00",
                },
                {
                    "Start time": "06-10-2016",
                    "End time": "07-10-2016",
                    "Hours": "6.67",
                    "Income": "0.00",
                    "First Check-In": "07-10-2016 08:45:00",
                    "Last Check-Out": "07-10-2016 15:25:00",
                },
                {
                    "Start time": "05-10-2016",
                    "End time": "06-10-2016",
                    "Hours": "8.08",
                    "Income": "0.00",
                    "First Check-In": "06-10-2016 08:15:00",
                    "Last Check-Out": "06-10-2016 16:20:00",
                },
                {
                    "Start time": "04-10-2016",
                    "End time": "05-10-2016",
                    "Hours": "7.50",
                    "Income": "0.00",
                    "First Check-In": "04-10-2016 09:10:00",
                    "Last Check-Out": "04-10-2016 16:40:00",
                }
            ],
            {
                # expected:
                48: {1: ['00:00']},
                40: {2: ['07:30'], 4: ['08:05'], 5: ['06:40']},
                35: {3: ['07:00']},
                'total_sum': 105300,
            },
            {
                # kwargs:
                "field_names": ["First Check-In", "Last Check-Out"],
                "datetime_parse_fmt": "%d-%m-%Y %H:%M:%S",
                "has_duration": False,
            }
        ),
        (
            [
                # input_data
                {
                    "Billable status": "Open / Not billable",
                    "Date": "25.07.2016",
                    "Day": "Mon",
                    "From": "0.00",
                    "To": "06:30",
                    "Break": "",
                    "Duration": "06:30",
                    "Project": "meh",
                    "Project no.": "lol",
                    "Activity": "Egen kompetansebygging/kurs",
                    "Comment": "Opplæring/introduksjon",
                    "Reason for declining": "",
                    "": "",
                },
            ],
            {
                # expected:
                'total_sum': 23400,
                30: {
                    1: ['06:30'],
                },
            },
            {
                # kwargs:
                "field_names": ["Date", "Duration"],
                "datetime_parse_fmt": "%d.%m.%Y",
                "has_duration": True,
            }
        ),
    ])
def test_valid_csv_reader_content(input_data, expected, kwargs):

    return_data = parse_csv_reader_content(
        input_data=input_data,
        **kwargs)

    assert return_data == expected


@pytest.mark.parametrize(
    "input_data,hours_per_week,expected",
    [
        (
            {
                # input_data
                'total_sum': 23400,
                30: {
                    1: ['06:30'],
                },
            },
            # {
            #     # work_days:
            #     "mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5,
            # },
            # hours_per_week
            40,
            {
                # expected
                'total_sum': 23400,
                'total_balance': 144000,
                'hours_per_week': 40.0,
                30: {
                    'balance': -120600,
                    1: ['06:30'],
                    'sum': 23400
                },
            },
        ),
        (
            {
                # input_data
                48: {1: ['00:00']},
                40: {2: ['07:30'], 4: ['08:05'], 5: ['06:40']},
                35: {3: ['07:00']},
                'total_sum': 18900,
            },
            # {
            #     # work_days:
            #     "mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5,
            # },
            # hours_per_week
            40,
            {
                # expected
                48: {
                    1: ['00:00'],
                    'sum': 0,
                    'balance': -144000,
                },
                40: {
                    'balance': -63900,
                    2: ['07:30'],
                    'sum': 80100,
                    4: ['08:05'],
                    5: ['06:40'],
                },
                35: {
                    3: ['07:00'],
                    'balance': -118800,
                    'sum': 25200
                },
                'total_balance': 345600,
                'total_sum': 18900,
                'hours_per_week': 40.0,
            },
        ),
    ])
def test_valid_parse_aggregate_weeks_and_weekdays(input_data, hours_per_week, expected):

    return_data = parse_aggregate_weeks_and_weekdays(
        aggregate_data=input_data,
        hours_per_week=hours_per_week, )

    assert return_data == expected

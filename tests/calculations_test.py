from os import path as op

# PIP import(s):
import pytest

# Module import(s):
from src.file_manip import get_csv_file_content_as_dicts
from src.calculations import parse_row


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

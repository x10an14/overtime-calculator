import os

# PIP import(s):
import pytest

# Module import(s):
from src.file_manip import get_csv_file_content_as_dicts


CSV_FILES_FOLDER = "tests/data"


@pytest.mark.parametrize(
    "file_name,expected",
    [
        ("header_and_one_row_1.csv",
            [
                {
                    "Start time": "27-11-2016",
                    "End time": "28-11-2016",
                    "Hours": "0.00",
                    "Income": "0.00",
                    "First Check-In": "28-11-2016 08:20:00",
                    "Last Check-Out": "28-11-2016 08:20:00"
                },
                {
                    "Start time": "31-08-2016",
                    "End time": "01-09-2016",
                    "Hours": "7.00",
                    "Income": "0.00",
                    "First Check-In": "31-08-2016 10:00:00",
                    "Last Check-Out": "31-08-2016 17:00:00"
                },
                {
                    "Start time": "06-10-2016",
                    "End time": "07-10-2016",
                    "Hours": "6.67",
                    "Income": "0.00",
                    "First Check-In": "07-10-2016 08:45:00",
                    "Last Check-Out": "07-10-2016 15:25:00"
                },
                {
                    "Start time": "05-10-2016",
                    "End time": "06-10-2016",
                    "Hours": "8.08",
                    "Income": "0.00",
                    "First Check-In": "06-10-2016 08:15:00",
                    "Last Check-Out": "06-10-2016 16:20:00"
                },
                {
                    "Start time": "04-10-2016",
                    "End time": "05-10-2016",
                    "Hours": "7.50",
                    "Income": "0.00",
                    "First Check-In": "04-10-2016 09:10:00",
                    "Last Check-Out": "04-10-2016 16:40:00"
                }]),
        ("header_and_one_row_2.csv",
            [{
                "Billable status": "Open / Not billable",
                "Date": "25.07.2016",
                "Day": "Mon",
                "From": "00:00",
                "To": "06:30",
                "Break": "",
                "": "",
                "Duration": "06:30",
                "Project": "meh",
                "Project no.": "lol",
                "Activity": "Egen kompetansebygging/kurs",
                "Comment": "Opplæring/introduksjon",
                "Reason for declining": ""
            }])
    ])
def test_valid_csv_files_parsing(file_name, expected):

    with open(os.path.join(CSV_FILES_FOLDER, file_name), "r") as f:
        return_dicts = get_csv_file_content_as_dicts(
            content=f.read(), file_name=file_name)

    # compare expected with returned:
    for x in expected:
        # Make sure all in expected are present in return_dicts
        assert x in return_dicts

    # compare returned with expected
    for x in return_dicts:
        # Make sure all in return_dicts are present in expected
        assert x in expected

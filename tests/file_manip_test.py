import os

# PIP import(s):
import pytest

# Module import(s):
from src.file_manip import get_csv_file_content_as_dicts


CSV_FILES_FOLDER = "tests/data"


@pytest.mark.parametrize(
    "file_name,compare_dict",
    [
        ("header_and_one_row_1.csv",
            {
                "Start time": "27-11-2016",
                "End time": "28-11-2016",
                "Hours": "0.00",
                "Income": "0.00",
                "First Check-In": "28-11-2016 08:20:00",
                "Last Check-Out": "28-11-2016 08:20:00"
            }),
        ("header_and_one_row_2.csv",
            {
                "Billable status": "Open / Not billable",
                "Date": "25.07.2016",
                "Day": "Mon",
                "From": "00:00",
                "To": "06:30",
                "Break": None,
                "Duration": "06:30",
                "Project": "870 Utvikling og drift",
                "Project no.": "00870",
                "Activity": "Egen kompetansebygging/kurs",
                "Comment": "Opplæring/introduksjon",
                "Reason for declining": None
            })
    ])
def test_valid_csv_files_parsing(file_name, compare_dict):

    with open(os.path.join(CSV_FILES_FOLDER, file_name), "r") as f:
        return_dicts = get_csv_file_content_as_dicts(
            content=f.read(), file_name=file_name)

    assert return_dicts == [compare_dict]

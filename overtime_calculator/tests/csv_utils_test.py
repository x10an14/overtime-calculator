from pathlib import Path

# PIP import(s):
import pytest

# Module import(s):
from overtime_calculator.src.csv_utils import get_csv_file_content_as_dicts

CSV_FILES_FOLDER = Path("overtime_calculator") / 'tests' / 'data'


@pytest.mark.parametrize(
    "file_name,expected",
    [
        ("header_and_five_rows.csv",
            [
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
                }]),
        ("header_and_one_row.csv",
            [{
                "Billable status": "Open / Not billable",
                "Date": "25.07.2016",
                "Day": "Mon",
                "From": "00:00",
                "To": "06:30",
                "Break": "",
                "Duration": "06:30",
                "Project": "meh",
                "Project no.": "lol",
                "Activity": "Egen kompetansebygging/kurs",
                "Comment": "Opplæring/introduksjon",
                "Reason for declining": "",
                '': '',
            }])
    ])
def test_valid_csv_files_parsing(file_name, expected):
    csv_file = Path(CSV_FILES_FOLDER) / file_name

    assert(csv_file.resolve(strict=True))
    return_dicts = get_csv_file_content_as_dicts(
        content=csv_file.read_text(encoding='utf-8'),
        file_name=file_name,
    )

    assert(len(return_dicts) == len(expected))
    assert(all(x in return_dicts for x in expected))


@pytest.mark.parametrize("file_name", ["empty_file.csv"])
def test_empty_csv_file_parsing(file_name):
    with pytest.raises(EOFError) as exc:
        csv_file = Path(CSV_FILES_FOLDER) / file_name

        assert(csv_file.resolve(strict=True))
        get_csv_file_content_as_dicts(
            content=csv_file.read_text(encoding='utf-8'),
            file_name=file_name,
        )

        assert exc.message == "File '{}' received is empty".format(file_name)


@pytest.mark.parametrize("file_name", ["three_rows_no_header.csv"])
def test_no_header_csv_file_parsing(file_name):
    with pytest.raises(NotImplementedError) as exc:
        csv_file = Path(CSV_FILES_FOLDER) / file_name
        assert(csv_file.resolve(strict=True))

        get_csv_file_content_as_dicts(
            content=csv_file.read_text(encoding='utf-8'),
            file_name=file_name,
        )

        assert exc.message == f"CSV file {file_name} has no CSV header!"


@pytest.mark.parametrize("file_name", ["header_only.csv"])
def test_header_only_csv_file_parsing(file_name):
    with pytest.raises(NotImplementedError) as exc:
        csv_file = Path(CSV_FILES_FOLDER) / file_name
        assert(csv_file.resolve(strict=True))

        get_csv_file_content_as_dicts(
            content=csv_file.read_text(encoding='utf-8'),
            file_name=file_name
        )

        message = f"Only one row found in {file_name}! "
        message += "Need header row + data rows!"
        assert exc.message == message

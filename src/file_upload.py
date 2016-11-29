"""Module for containing file utilities."""
import csv
import logging
from tempfile import SpooledTemporaryFile

# PIP import:
from sanic.response import json


def get_uploaded_csv_file_content(content, file_name, encoding='utf-8', tempfile_func=SpooledTemporaryFile):
    input_file_content = content.decode(encoding)
    file_length = len(input_file_content)
    with SpooledTemporaryFile(
            file_length,
            mode="rw",
            encoding=encoding) as f:
        # save content to temporary file in memory (not disk)
        length = f.write(input_file_content)
        if length == 0:
            logging.error("File ({}) received is empty.".format(file_name))
            return json(dict(response="no content in uploaded file"))
        # Reset file-read
        f.seek(0)
        logging.info("Content written to tempfile...")

        # decide dialect:
        dialect = csv.Sniffer().sniff(f.read())
        f.seek(0)
        logging.debug("CSV dialect '{}' sniffed...".format(dialect))

        # read csv:
        reader = csv.DictReader(f, dialect=dialect)
        saved_content = list(reader)

    return saved_content

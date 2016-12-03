"""Module for containing file utilities."""
import csv
import logging
from tempfile import SpooledTemporaryFile

# Module import
from . import log_function_entry_and_exit


@log_function_entry_and_exit
def get_csv_file_content_as_dicts(content, file_name, encoding='utf-8', tempfile_func=SpooledTemporaryFile):
    """Function for sniffing CSV dialect and returning content as list of dicts per row."""
    # input_file_content = content.encode(encoding)
    file_length = len(content)

    if file_length == 0:
        logging.error("File ({}) received is empty.".format(file_name))
        raise EOFError

    with SpooledTemporaryFile(
            file_length,
            mode="rw") as f:
        # save content to temporary file in memory (not disk)
        length = f.write(content)
        assert length == file_length

        # Reset file-read to start of file
        f.seek(0)
        logging.info("Content written to tempfile...")

        # Sniff read length:
        sniff_length = int(length / 2)

        # Ensure file has header:
        if not csv.Sniffer().has_header(f.read(sniff_length)):
            logging.error("CSV file {} has no CSV header!".format(file_name))
            raise NotImplementedError
        logging.info("CSV header found...")

        # decide dialect:
        dialect = csv.Sniffer().sniff(f.read(sniff_length))
        f.seek(0)
        logging.debug("CSV dialect '{}' sniffed...".format(dialect))
        logging.info(r"Delimiter: '{}', Line separator: {}".format(
            dialect.delimiter, dialect.lineterminator.encode('unicode_escape')))

        # read csv:
        reader = csv.DictReader(f, dialect=dialect)
        saved_content = list(reader)

    if len(saved_content) <= 1:
        logging.error(
            "Only one row found in {}! Need header row + data rows!".format(
                file_name))
        raise NotImplementedError

    return saved_content

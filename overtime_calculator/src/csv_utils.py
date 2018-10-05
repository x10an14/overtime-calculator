"""Module for containing file utilities."""
import csv
import logging

# Module import
from . import log_function_entry_and_exit


@log_function_entry_and_exit
def get_csv_file_content_as_dicts(
    content,
    file_name,
    *,
    encoding='utf-8',
    tempfile_func=None,
):
    """Function for sniffing CSV dialect and returning content as list of dicts per row."""
    if tempfile_func is None:
        from tempfile import SpooledTemporaryFile
        tempfile_func = SpooledTemporaryFile

    # input_file_content = content.encode(encoding)
    file_length = len(content)

    if file_length == 0:
        message = "File '{}' received is empty.".format(file_name)
        logging.error(message)
        raise EOFError(message)

    with SpooledTemporaryFile(
            file_length,
            mode="rw",
            encoding=encoding,
    ) as f:
        # save content to temporary file in memory (not disk)
        length = f.write(content)
        assert length == file_length

        # Reset file-read to start of file
        logging.info("Content written to tempfile...")
        f.seek(0)

        # Sniff read length:
        sniff_length = int(length / 2)

        # Ensure file has header:
        if not csv.Sniffer().has_header(f.read(sniff_length)):
            message = "CSV file {} has no CSV header!".format(file_name)
            logging.error(message)
            raise NotImplementedError(message)
        logging.info("CSV header found...")
        f.seek(0)

        # decide dialect:
        dialect = csv.Sniffer().sniff(f.read(sniff_length))
        logging.debug("CSV dialect '{}' sniffed...".format(dialect))
        logging.info(r"Delimiter: '{}', Quotechar: '{}', Line separator: {}".format(
            dialect.delimiter,
            dialect.quotechar,
            dialect.lineterminator.encode('unicode_escape')))
        f.seek(0)

        # read csv:
        reader = csv.DictReader(f, dialect=dialect)
        saved_content = list(reader)

    if len(saved_content) < 1:
        message = "Only one row found in {}! ".format(file_name)
        message += "Need header row + data rows!"
        logging.error(message)
        raise NotImplementedError(message)

    logging.debug("Returning: {}".format(saved_content))
    return saved_content if type(saved_content) is list else [saved_content]

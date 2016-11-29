"""Webapp start-up python script for Overtime-Calculator."""
import csv
import json
import logging
from tempfile import SpooledTemporaryFile

# PIP imports:
from sanic.response import json as sanicjson

# Module imports:
from src import app
from src import _serialize_json
from src import default_parse_fmt
from src import log_function_entry_and_exit
from src.calculations import parse_csv_reader_content
from src.calculations import parse_aggregate_weeks_and_weekdays


@app.route("/hello")
@log_function_entry_and_exit
def _test(request):
    return sanicjson({"hello": "world"})


@app.route("/files")
@log_function_entry_and_exit
def _post_json(request):

    def get_file_data_from_request_as_dict(request_data):
        return dict(
            body=request_data.body,
            name=request_data.name,
            type=request_data.type, )

    func = get_file_data_from_request_as_dict
    files_parameters = [func(x) for x in request.files.keys()]

    return_dict = dict(
        received=True,
        file_names=request.files.keys(),
        test_file_parameters=files_parameters, )

    return sanicjson(return_dict)


@app.route("/rest_request")
@log_function_entry_and_exit
def _return_rest_request(request):
    return_dict = request
    return sanicjson(return_dict)


@app.route("/csv_upload")
@log_function_entry_and_exit
def calculate_csv(request):
    logging.info("Receiving a request to {}".format(request.url))

    # uploaded_files = request.files.items()
    print("Received the following files:")

    files = request.files
    print("\t#of files: {}, file_names: {}".format(
        len(files),
        [(x, y.name) for x, y in files.items()]))

    # select one file of potentially more than one
    keys = list(files.keys())
    selected_key = keys[0]
    if len(files) > 1:
        # Necessary to support indexing
        for key in keys:
            if "csv" in key.lower():
                selected_key = key

    # input_file_name = files[selected_key].name
    input_file_content = files[selected_key].body
    input_file_content = input_file_content.decode('utf-8')
    tempfile = SpooledTemporaryFile(
        max_size=len(input_file_content),
        mode="rw")

    # save content to temporary file in memory (not disk)
    length = tempfile.write(input_file_content)
    if length == 0:
        print("File ({}) received is empty.".files[selected_key].name)
        return sanicjson(dict(response="no content in uploaded file"))

    # Reset file-read
    tempfile.seek(0)
    print("Content writtent to tempfile...")

    # decide dialect:
    dialect = csv.Sniffer().sniff(tempfile.read())
    tempfile.seek(0)
    print("CSV dialect '{}' sniffed...".format(dialect))

    # read csv:
    reader = csv.DictReader(tempfile, dialect=dialect)
    parsed_content = list(reader)
    print("#rows in csv_file: {}".format(len(parsed_content)))

    print("Parsing time records...")
    aggregate_records, overtime_records = parse_csv_reader_content(
        csv_reader=parsed_content)
    print("Parsing time records more deeply...")
    aggregate_records = parse_aggregate_weeks_and_weekdays(
        aggregate_data=aggregate_records)
    print("Done parsing!")

    return_dict = dict(
        aggregate_records=aggregate_records,
        overtime_records=overtime_records)

    return_dict = json.dumps(return_dict, default=_serialize_json)

    print("Returning parsed records.")
    return sanicjson(dict(response="ok", return_dict=return_dict))


if __name__ == '__main__':
    debug = True

    logging_format = "%(asctime)s[%(process)d]%(levelname)s::%(module)s:%(lineno)d: "
    logging.basicConfig(
        level=logging.INFO,
        format=logging_format,
        datefmt=default_parse_fmt, )

    app.run(host="127.0.0.1", port=8000, debug=debug)

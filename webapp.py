"""Webapp start-up python script for Overtime-Calculator."""
import csv
# import logging    # TODO: Implement logging...
from tempfile import SpooledTemporaryFile

# PIP imports:
from sanic.response import json

# Module imports:
from src import app
from src import parse_csv_reader_content
from src import parse_aggregate_weeks_and_weekdays


@app.route("/hello")
def _test(request):
    return json({"hello": "world"})


@app.route("/files")
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

    return json(return_dict)


@app.route("/rest_request")
def _return_rest_request(request):
    return_dict = request
    return json(return_dict)


@app.route("/csv_upload")
def calculate_csv(request):
    from IPython import embed
    print("Receiving a request to {}".format(request.url))

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
        return json(dict(response="no content in uploaded file"))

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

    print("Returning parsed records.")
    embed()
    return json(dict(response="ok", return_dict=return_dict))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)

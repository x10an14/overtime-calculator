"""Webapp start-up python script for Overtime-Calculator."""
import json
import logging

# PIP imports:
from sanic.response import json as sanicjson

# Module imports:
from src import _serialize_json
from src import app
from src import default_parse_fmt
from src import log_function_entry_and_exit
from src.calculations import parse_csv_reader_content
from src.calculations import parse_aggregate_weeks_and_weekdays
from src.file_upload import get_uploaded_csv_file_content


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
    logging.info("Received the following files:")

    files = request.files
    logging.info("\t#of files: {}, file_names: {}".format(
        len(files),
        [(x, y.name) for x, y in files.items()]))

    if len(files) != 1:
        logging.error(
            "Received {} files, can only accept receiving 1 (not 0) file.".format(
                len(files)))
        return sanicjson(dict(
            response="Need one (and only one) csv file uploaded for this to work!"))

    selected_key = list(files.keys())[0]
    saved_content = get_uploaded_csv_file_content(
        content=files[selected_key].body,
        file_name=files[selected_key].name)
    logging.info("#rows in csv_file: {}".format(len(saved_content)))

    logging.info("Parsing time records...")
    aggregate_records, overtime_records = parse_csv_reader_content(
        csv_reader=saved_content)

    logging.debug("Parsing time records more deeply...")
    aggregate_records = parse_aggregate_weeks_and_weekdays(
        aggregate_data=aggregate_records)
    logging.info("Done parsing!")

    # Serialize data structures to json format
    logging.info("Serializing data structures to json-string...")
    return_dict = dict(
        overtime_records=overtime_records,
        aggregate_records=aggregate_records,)
    return_dict = json.dumps(return_dict, default=_serialize_json)
    logging.info("Done serializing data structures to json-string!")

    logging.info("Returning parsed records...")
    return sanicjson(dict(response="ok", return_dict=return_dict))


if __name__ == '__main__':
    debug = True

    logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
    logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
    logging_format += "%(message)s"
    logging.basicConfig(
        format=logging_format,
        datefmt=default_parse_fmt + "%f",
        level=logging.DEBUG if debug else logging.INFO, )

    app.run(host="127.0.0.1", port=8000, debug=debug)

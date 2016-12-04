"""Webapp start-up python script for Overtime-Calculator."""
import logging

# PIP imports:
from sanic.response import json as sanic_json
from sanic.response import text as sanic_text
from sanic.response import html as sanic_html
from jinja2 import Environment, PackageLoader

# Module imports:
from src import app
from src import log_function_entry_and_exit
from src.calculations import parse_csv_reader_content
from src.calculations import parse_aggregate_weeks_and_weekdays
from src.file_manip import get_csv_file_content_as_dicts


@app.route("/hello")
@log_function_entry_and_exit
def _test(request):
    env = Environment(loader=PackageLoader('src', 'templates'))
    template = env.get_template("basic.html")
    # return sanic_json({"hello": "world"})
    # return sanic_text("Hello world!")
    a = template.render(a=dict(hello="world"))
    return sanic_html(a)


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

    return sanic_json(return_dict)


@app.route("/rest_request")
@log_function_entry_and_exit
def _return_rest_request(request):
    return_dict = request
    return sanic_json(return_dict)


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
        return sanic_json(dict(
            response="Need one (and only one) csv file uploaded for this to work!"))

    selected_key = list(files.keys())[0]
    saved_content = get_csv_file_content_as_dicts(
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

    return_dict = dict(
        overtime_records=overtime_records,
        aggregate_records=aggregate_records,)
    logging.info("Returning parsed records...")
    return sanic_json(dict(return_dict))


if __name__ == '__main__':
    debug = True

    default_time_fmt = "%d-%m-%Y %H:%M:%S"
    logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
    logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
    logging_format += "%(message)s"
    logging.basicConfig(
        format=logging_format,
        datefmt=default_time_fmt + "%f",
        level=logging.DEBUG if debug else logging.INFO, )

    app.run(host="127.0.0.1", port=8000, debug=debug)

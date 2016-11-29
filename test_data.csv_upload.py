"""Small script to test uploading a .csv file."""
import json
from sys import argv

# PIP imports:
import requests

default_base_url = "http://127.0.0.1:8000"
default_endpoint = "/csv_upload"


if __name__ == '__main__':
    request_url = "{}{}".format(default_base_url, default_endpoint)
    if len(argv) < 2:
        print("\nNeed a csv file given as first parameter!\n\n")
        raise NotImplementedError
    input_file = open(argv[1], "r")
    response = requests.post(request_url, files=dict(csv_file=input_file))

    json_data = response.json()
    return_data = sorted(json.loads(json_data['return_dict']).items())
    print(return_data)

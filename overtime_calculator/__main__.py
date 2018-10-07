import sys
import pathlib

import hug

from overtime_calculator import auth, api


@hug.get("/", output=hug.output_format.html)
def base():
    return "<h1>Hello, world</h1>"


@hug.extend_api()
def with_other_apis():
    return [
        auth,
        api
    ]

if __name__ == '__main__':
    _file = pathlib.Path(sys.argv[0])
    module = _file.parent.name
    print(
        f"Start {module} with Hug, like so: hug --file {_file}",
        file=sys.stderr,
    )
    sys.exit(1)

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

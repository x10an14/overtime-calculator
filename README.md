# Overtime-Calculator
Personal attempt at simplifying the calculation of what I've accumulated (potentially deficit) over-time!

## Tests:
The tests lie in the `tests/` folder inside the git repo.
Any data used for integration testing lies inside `tests/data/`.

### Run (just) tests:
py.test is used, and lies in requirements.txt.
To execute, run the below command from the root of the git repo:
`venv/bin/python setup.py test`

### Run test Coverage:
Coverage is used, and included in requirements.txt.
See below for how to use:
`venv/bin/coverage run setup.py test`

#### To get Coverage report:
Use below command:
`venv/bin/coverage html`

To open HTML up in Google Chrome from terminal:
`google-chrome htmlcov/index.html`

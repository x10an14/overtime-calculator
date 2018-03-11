# Overtime-Calculator
Hobby programming project, with the intent of simplifying overtime calculation(s).

### Major dependencies:
1. (https://github.com/timothycrosley/hug/)[Hug]
2. (https://github.com/HypothesisWorks/hypothesis-python)[Hypothesis]

### Intended features:
- [ ] Read in input from CSV files
  * (Rows of "start time" and "end time")
- [ ] Have it keep track of current surplus/deficit
  * [ ] Have it also keep track of surplus/deficit _per_ week
  * [ ] Specify desired surplus/deficit to aim for (maybe also deadline so as to aim for a vacation?)
- [ ] Display these intended features in a simple web GUI
  * (Maybe do this in a separate NodeJS repo?)
- [ ] Split out library logic into its own git repo

## Tests:
The tests are composed by with the Hypothesis framework, and run with (https://github.com/pytest-dev/pytest)[py.test].
The tests should lie in the `tests/` folder inside the git repo.
Any data used for integration testing lies inside `tests/data/`.

### Run (just) tests:
py.test is used, and lies in requirements.txt.
To execute, run the below command from the root of the git repo:
`pipenv run python setup.py test`

### Run test Coverage:
Coverage is used, and included in requirements.txt.
See below for how to use:
`pipenv run coverage run setup.py test`

#### To get Coverage report:
`pipenv run coverage html`

To open HTML up in Google Chrome from terminal:
`google-chrome htmlcov/index.html`

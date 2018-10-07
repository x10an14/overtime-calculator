# Overtime-Calculator
[![Build Status](https://travis-ci.org/x10an14/overtime-calculator.svg?branch=master)](https://travis-ci.org/x10an14/overtime-calculator)
[![Coverage Status](https://coveralls.io/repos/github/x10an14/overtime-calculator/badge.svg?branch=master)](https://coveralls.io/github/x10an14/overtime-calculator?branch=master)

Hobby programming project, with the intent of simplifying overtime calculation(s).

### Major dependencies:
- [Hug](https://github.com/timothycrosley/hug)
- [Pipenv](https://github.com/pypa/pipenv)
- [Hypothesis](https://github.com/HypothesisWorks/hypothesis-python)

### Intended features:
- [ ] Read in input from CSV files
  * (Rows of "start time" and "end time")
- [ ] Have it keep track of current surplus/deficit
  * [ ] Have it also keep track of surplus/deficit _per_ week
  * [ ] Specify desired surplus/deficit to aim for (maybe also deadline so as to aim for a vacation?)
- [ ] Display these intended features in a simple web GUI
  * (Maybe do this in a separate NodeJS repo?)
- [ ] Split out library logic

### CLI

* Run (just) tests: `pipenv run python -m pytest tests`
  - py.test is used, and lies in `Pipfile`. Execute command from git repo root.
* Run test Coverage: `make test` (Runs above test-command _and_ creates coverage report).
* Open coverage report in browser: `pipenv run coverage html && <browser> htmlcov/index.html`
  - Requires you to have run the equivalent of `python -m coverage report -m`, which `make test` does.

### Tests:
The tests are composed by with the Hypothesis framework, and run with [py.test](https://github.com/pytest-dev/pytest).
The tests should lie in the `tests/` folder inside the git repo.
Any data used for integration testing lies inside `tests/data/`.

python_files := $(shell find overtime_calculator/ tests/ -type f -name '*.py')

all: install html_test_report

.PHONY: install
install: Pipfile
	sudo aptitude install build-essential libssl-dev libffi-dev python3.7-dev
	pipenv install --dev

# TODO: Figure out how to add 'install'-rule as pre-requisite
.PHONY: test
test: $(python_files)
	pipenv run python -m coverage run -m py.test
	pipenv run python -m coverage report -m

check_for_dead_code:
	pipenv run vulture ./overtime_calculator ./tests

.PHONY: html_test_report
html_test_report: test
	pipenv run python -m coverage html

.PHONY: check_pep8
check_pep8: $(python_files)
	pipenv run python -m flake8

.PHONY: start_api
start_api: $(python_files)
	pipenv run hug --file ./overtime_calculator/__main__.py

.PHONY: release lock
lock release: Pipfile
	pipenv lock
	git add Pipfile.lock

.PHONY: clean
clean:
	rm -rf .pytest_cache .hypothesis htmlcov .coverage
	# https://unix.stackexchange.com/a/115869:
	find . -type d -name __pycache__ -prune -exec rm -rf {} \;
	find . -type f -regextype sed -regex ".*\.py[cod]" -exec rm {} \;

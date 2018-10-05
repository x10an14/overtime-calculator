.PHONY: install pre_release release lock test html_test_report clean check_pep8 start_api

python_files := $(shell find overtime_calculator/ -name '*.py')

all: install html_test_report

install: Pipfile
	sudo aptitude install build-essential libssl-dev libffi-dev python3.6-dev
	pipenv install --dev

# TODO: Figure out how to add 'install'-rule as pre-requisite
test: $(python_files)
	pipenv run python -m coverage run -m py.test
	pipenv run python -m coverage report -m

check_for_dead_code:
	pipenv run vulture ./overtime_calculator

html_test_report: test
	pipenv run python -m coverage html

check_pep8: $(python_files)
	pipenv run python -m flake8 overtime_calculator

start_api: $(python_files)
	pipenv run hug -f overtime_calculator/src/api.py

pre_release: Pipfile
	pipenv lock --pre

lock release: Pipfile
	pipenv lock
	git add Pipfile.lock

clean:
	rm -rf .pytest_cache .hypothesis htmlcov
	# https://unix.stackexchange.com/a/115869:
	find . -type d -name __pycache__ -prune -exec rm -rf {} \;
	find . -type f -regextype sed -regex ".*\.py[cod]" -exec rm {} \;

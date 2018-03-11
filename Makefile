.PHONY: install pre_release release lock test html_test_report check_minimum_coverage clean

python_files := $(shell find overtime_calculator/ -name '*.py')

all: install html_test_report

install: Pipfile $(python_files)
	pipenv install --dev

test: Pipfile $(python_files)
	pipenv run python -m coverage run \
	--branch \
	--source=overtime_calculator \
	--omit=overtime_calculator/setup.py \
	-m py.test
	pipenv run python -m coverage report

coverage_threshold := "70"
check_minimum_coverage:
	# https://stackoverflow.com/a/14605330
	pipenv run python -m coverage report | egrep '^TOTAL' | pipenv run python \
	bin/compare_numbers.py $(coverage_threshold)

html_test_report: test
	pipenv run python -m coverage html

pre_release: Pipfile
	pipenv lock --pre

lock release: Pipfile
	pipenv lock

clean:
	rm -rf .pytest_cache .hypothesis htmlcov
	# https://unix.stackexchange.com/a/115869:
	find . -type d -name __pycache__ -prune -exec rm -rf {} \;
	find . -type f -regextype sed -regex ".*\.py[cod]" -exec rm {} \;

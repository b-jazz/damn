#* Variables
SHELL := /usr/bin/env bash
PYTHON := python
PYTHONPATH := `pwd`

#* Developer Setup - bring in code check/format/package tools
.PHONY: dev-install
dev-install:
	pipenv install --dev black pyupgrade isort setuptools

#* Installation
.PHONY: install
install:
	pipenv lock -n && pipenv export --without-hashes > requirements.txt
	pipenv install -n
	-pipenv run mypy --install-types --non-interactive ./

.PHONY: pre-commit-install
pre-commit-install:
	pipenv run pre-commit install

#* Formatters
.PHONY: codestyle
codestyle:
	pipenv run pyupgrade --exit-zero-even-if-changed --py313-plus **/*.py
	pipenv run isort --settings-path pyproject.toml ./
	pipenv run black --config pyproject.toml ./

.PHONY: formatting
formatting: codestyle

#* Linting
.PHONY: test
test:
	PYTHONPATH=$(PYTHONPATH) pipenv run pytest -c pyproject.toml --cov-report=html --cov=dam_monitor tests/
	pipenv run coverage-badge -o assets/images/coverage.svg -f

.PHONY: check-codestyle
check-codestyle:
	pipenv run isort --diff --check-only --settings-path pyproject.toml ./
	pipenv run black --diff --check --config pyproject.toml ./
	pipenv run darglint --verbosity 2 dam_monitor tests

.PHONY: mypy
mypy:
	pipenv run mypy --config-file pyproject.toml ./

.PHONY: check-safety
check-safety:
	pipenv check
	pipenv run safety check --full-report
	pipenv run bandit -ll --recursive dam_monitor tests

.PHONY: lint
lint: test check-codestyle mypy check-safety

.PHONY: update-dev-deps
update-dev-deps:
	pipenv add -D bandit@latest darglint@latest "isort[colors]@latest" mypy@latest pre-commit@latest pydocstyle@latest pylint@latest pytest@latest pyupgrade@latest safety@latest coverage@latest coverage-badge@latest pytest-html@latest pytest-cov@latest
	pipenv add -D --allow-prereleases black@latest

#* Cleaning
.PHONY: pycache-remove
pycache-remove:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

.PHONY: dsstore-remove
dsstore-remove:
	find . | grep -E ".DS_Store" | xargs rm -rf

.PHONY: mypycache-remove
mypycache-remove:
	find . | grep -E ".mypy_cache" | xargs rm -rf

.PHONY: ipynbcheckpoints-remove
ipynbcheckpoints-remove:
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf

.PHONY: pytestcache-remove
pytestcache-remove:
	find . | grep -E ".pytest_cache" | xargs rm -rf

.PHONY: build-remove
build-remove:
	rm -rf build/

.PHONY: cleanup
cleanup: pycache-remove dsstore-remove mypycache-remove ipynbcheckpoints-remove pytestcache-remove

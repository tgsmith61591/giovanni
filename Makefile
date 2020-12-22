SHELL := /bin/bash
PYTHON ?= python
CWD = $(shell pwd)

REPO := giovanni

# Source git tag/hash info
include $(CWD)/dist.mk
include $(CWD)/git.mk
include $(CWD)/lint.mk

.PHONY: clean
clean:
	rm -rf dist
	rm -rf build
	rm -rf .pytest_cache
	rm -rf $(REPO).egg-info
	rm -f $(REPO)/VERSION
	rm -rf .coverage
	rm -rf .coverage.*

.PHONY: requirements
requirements:
	$(PYTHON) -m pip install -r requirements.txt

.PHONY: testing-requirements
testing-requirements:
	$(PYTHON) -m pip install pytest coverage pytest-cov codecov

.PHONY: test-unit
test-unit:
	$(PYTHON) -m pytest -v --durations=20 --cov-config .coveragerc --cov $(REPO)

.PHONY: test
test: test-lint test-unit

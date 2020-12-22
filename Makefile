SHELL := /bin/bash
PYTHON ?= python
CWD = $(shell pwd)

# Source git tag/hash info
include $(CWD)/git.mk
include $(CWD)/lint.mk

REPO := dexter

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

.PHONY: sdist
sdist: version
	$(PYTHON) setup.py sdist

.PHONY: testing-requirements
testing-requirements:
	$(PYTHON) -m pip install pytest coverage pytest-cov codecov

.PHONY: test-unit
test-unit:
	$(PYTHON) -m pytest -v --durations=20 --cov-config .coveragerc --cov $(REPO)

# Version is created on tag
.PHONY: version
version:
ifneq ($(RELEASE_TAG),)
	echo "Tag is $(RELEASE_TAG)"
	echo $(RELEASE_TAG) > $(CWD)/$(REPO)/VERSION
else
	echo "Not a tagged commit, will not write to VERSION file"
	exit 1
endif

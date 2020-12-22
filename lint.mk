SHELL := /bin/bash

# Defines a PHONY target for linting, irrespective of where in the package you
# are running this from. Note that it depends on the CWD variable, which is
# defined in the Makefiles that include this.

FLAKE8_VERSION ?= 3.8.4

.PHONY: lint-requirements
lint-requirements:
	$(PYTHON) -m pip install flake8==$(FLAKE8_VERSION)

# 1. Ignore unused import in __init__
# 2. Ignore 'import *' in __init__
# 3. Limit line lenth to 79
# 4. Ignore several other errors globally

.PHONY: test-lint
test-lint:
	$(PYTHON) -m flake8 $(CWD) \
		--filename='*.py' \
		--per-file-ignores='*__init__.py:F401,F403' \
		--max-line-length=79 \
		--ignore W293,W504,E402,W605 \
		--doctests

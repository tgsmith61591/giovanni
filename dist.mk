SHELL := /bin/bash

# To create a release:
#
#  $ RELEASE_TAG=x.x.x make version
#  $ make sdist
#  $ make deploy
#
# Note that this depends on the proper environmentals existing, so not just anyone
# can do this.

.PHONY: version
version:
ifneq ($(RELEASE_TAG),)
	echo "Tag is $(RELEASE_TAG)"
	echo $(RELEASE_TAG) > $(CWD)/$(REPO)/VERSION
else
	echo "Not a tagged commit, will not write to VERSION file"
	exit 1
endif

.PHONY: deploy-requirements
deploy-requirements:
	$(PYTHON) -m pip install wheel twine

.PHONY: sdist
sdist:
	$(PYTHON) setup.py sdist

.PHONY: deploy
deploy:
ifneq ("$(wildcard $(CWD)/$(REPO)/VERSION)","")
	$(PYTHON) -m twine upload --skip-existing dist/$(REPO)-*
else
	echo "Not a tagged commit, will not deploy"
	exit 1
endif

SHELL := /bin/bash

GIT_HASH = $(shell git rev-parse --verify HEAD)
GIT_TAG := $(shell git describe --tags --exact-match $(GIT_HASH) 2>/dev/null)

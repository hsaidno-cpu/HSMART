PYTHON ?= python

.PHONY: install test validate

install:
	$(PYTHON) -m pip install -r requirements-dev.txt

test:
	$(PYTHON) -m pytest -q

validate: test

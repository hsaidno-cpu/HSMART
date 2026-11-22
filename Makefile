PYTHON ?= python

.PHONY: install check-python validate-json test pip-check validate

install:
	$(PYTHON) -m pip install -r requirements-dev.txt

check-python:
	$(PYTHON) -c "import sys; assert sys.version_info[:2] == (3, 12), sys.version"

validate-json:
	$(PYTHON) scripts/validate-json.py

test: check-python
	$(PYTHON) -m pytest -q

pip-check:
	$(PYTHON) -m pip check

validate: validate-json test pip-check

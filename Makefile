PY=python

.PHONY: test

test:
	$(PY) -m pytest -q tests -v

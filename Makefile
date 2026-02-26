PY=python

.PHONY: test run-worker run-cli

test:
	$(PY) -m pytest -q tests -v

run-worker:
	$(PY) -m llm_structured_extract_service.worker worker -l info -Q extract

run-cli:
	$(PY) -m llm_structured_extract.cli --text "张三，邮箱 zhang@example.com，电话 13800001234"

run_tests:
	uv run pytest -vv


provision:
	uv run python ops/kafka/provision.py
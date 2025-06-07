run_tests:
	uv run pytest -vv


provision:
	uv run python ops/kafka/provision.py


producer_start:
	uv run --directory src -m main start-producer
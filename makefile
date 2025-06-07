run_tests:
	uv run pytest -vv


provision:
	uv run python ops/kafka/provision.py


producer:
	uv run --directory src -m main start-producer

consumer:
	uv run --directory src -m main start-consumer
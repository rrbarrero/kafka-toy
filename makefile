SHELL := /usr/bin/bash
.ONESHELL:

run_tests:
	uv run pytest -vv

provision:
	uv run python ops/kafka/provision.py

producer:
	uv run --directory src -m main start-producer

consumer:
	uv run --directory src -m main start-consumer

play:
	echo "Starting producer and consumer. Ctrl+C to stop both."
	trap 'echo "\n🛑 Stopping producer and consumer…"; kill 0' SIGINT
	uv run --directory src -m main start-producer &
	uv run --directory src -m main start-consumer &
	wait
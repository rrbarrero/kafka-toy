import threading
import time
import typer
from factory import (
    create_consumer_service,
    create_producer_service,
)


app = typer.Typer()


@app.command()
def start_producer():
    create_producer_service().start()


def run_consumer(name: str):
    service = create_consumer_service(name)
    service.start()


@app.command()
def start_consumer():

    names = ["🔵 ZULU", "🟣 BRAVO"]
    threads = []
    for n in names:
        t = threading.Thread(
            target=run_consumer, args=(n,), daemon=True, name=f"consumer-{n}"
        )
        t.start()
        threads.append(t)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Shutting down all consumers (Ctrl+C pressed).")


@app.callback()
def main():
    """Fix: Got unexpected extra argument (start-producer)"""
    pass


if __name__ == "__main__":
    app()

import threading
import time
import typer
from factory import (
    create_consumer_service_bravo,
    create_consumer_service_zulu,
    create_producer_service,
)


app = typer.Typer()


@app.command()
def start_producer():
    create_producer_service().start()


def run_consumer(name: str):
    match name:
        case "🔵 ZULU":
            service = create_consumer_service_zulu(name)
        case "🟣 BRAVO":
            service = create_consumer_service_bravo(name)
        case _:
            raise ValueError(f"Invalid consumer name: {name}")

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

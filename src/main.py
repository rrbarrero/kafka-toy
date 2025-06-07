import typer
from factory import create_kafka_consumer_repository, create_producer_service

app = typer.Typer()


@app.command()
def start_producer():
    create_producer_service().start()


@app.command()
def run_consumer():
    print(create_kafka_consumer_repository().pull_queue())


@app.callback()
def main():
    """Fix: Got unexpected extra argument (start-producer)"""
    pass


if __name__ == "__main__":
    app()

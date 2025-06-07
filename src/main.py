import typer
from factory import create_producer_service

app = typer.Typer()


@app.command()
def start_producer():
    create_producer_service().start()


@app.callback()
def main():
    """Fix: Got unexpected extra argument (start-producer)"""
    pass


if __name__ == "__main__":
    app()

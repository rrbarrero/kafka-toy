from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path
import os


@dataclass
class Settings:
    kafka_host_ip: str
    port: int
    transaction_topic: str = "transactions"

    @classmethod
    def from_env(cls):
        project_path = Path(__file__).parent.parent
        load_dotenv(project_path / ".env")

        return cls(
            kafka_host_ip=os.getenv("KAFKA_HOST_IP", "localhost"),
            port=int(os.getenv("KAFKA_PORT", "9092")),
        )

    @property
    def kafka_host(self):
        return f"{self.kafka_host_ip}:{self.port}"


settings = Settings.from_env()

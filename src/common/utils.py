from config import settings
import json


def load_fixture(fixture_name):
    with open(f"{settings.fixture_path}/{fixture_name}") as fr:
        return json.load(fr)

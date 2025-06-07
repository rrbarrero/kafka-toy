import pytest
from factory import create_kafka_repository


@pytest.mark.acceptance
def test_needed_topics_are_created():
    repo = create_kafka_repository()

    assert "testing_topic" in repo.list_topics()

import pytest
from factory import create_kafka_consumer_repository


@pytest.mark.acceptance
def test_needed_topics_are_created():
    repo = create_kafka_consumer_repository("testing")

    assert "testing_topic" in repo.list_topics()

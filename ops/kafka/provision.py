from kafka.admin import KafkaAdminClient, NewTopic
from config import settings

admin_client = KafkaAdminClient(
    bootstrap_servers=settings.kafka_host,
    client_id="test_admin",
)

topic_list = [NewTopic(name="mi_topic", num_partitions=3, replication_factor=1)]

try:
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
    print("Topic created succesfully")
except Exception as e:
    print(f"Error creating topic: {e}")

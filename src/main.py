from factory import create_kafka_repository


def main():
    repo = create_kafka_repository()
    topics = repo.list_topics()
    print(topics)


if __name__ == "__main__":
    main()

from infra.KafkaRepository import KafkaRepository


def main():
    repo = KafkaRepository.from_env()
    topics = repo.list_topics()
    print(topics)


if __name__ == "__main__":
    main()

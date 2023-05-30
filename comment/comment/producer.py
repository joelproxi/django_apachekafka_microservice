from confluent_kafka import Producer


conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "blog",
    "auto.offset.reset": "earliest",
}

producer = Producer(conf)

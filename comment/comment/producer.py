from confluent_kafka import Producer


conf = {
    "bootstrap.servers": "localhost:8001",
    "groupe.id": "blog",
    "auto.offset.reset": "earliest",
}

producer = Producer(conf)

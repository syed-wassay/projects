import json
import os
import pickle

import sklearn.ensemble
from base_logger import logger
from kafka import KafkaConsumer, KafkaProducer


class PredictionService:
    def __init__(self):
        self.kafka_server = os.environ.get("KAFKA_SERVER")
        self.consumer_topic = os.environ.get("CONSUMER_TOPIC")
        self.producer_topic = os.environ.get("PRODUCER_TOPIC")
        self.model_filename = os.environ.get("MODEL_FILENAME")

        if None in (
            self.kafka_server,
            self.consumer_topic,
            self.producer_topic,
            self.model_filename,
        ):
            error_msg = "You need to specify KAFKA_SERVER, CONSUMER_TOPIC, PRODUCER_TOPIC, MODEL_FILENAME"
            logger.error(error_msg)
            raise Exception(error_msg)

        self.model_path = os.path.join(os.getcwd(), self.model_filename)
        if not os.path.exists(self.model_path):
            error_msg = f"Could not find model at {self.model_path}"
            logger.error(error_msg)
            raise Exception(error_msg)

        self.model = self.load_model()

        self.consumer = KafkaConsumer(
            self.consumer_topic,
            group_id="apply-predictions",
            enable_auto_commit=False,
            auto_offset_reset="earliest",
            bootstrap_servers=self.kafka_server,
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )

        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_server,
            acks=1,
            value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
        )

    def load_model(self) -> sklearn.ensemble._forest.RandomForestClassifier:
        with open(self.model_path, "rb") as f:
            return pickle.load(f)

    def get_prediction(self, X) -> int:
        result = self.model.predict(X)
        return result[0]

    def send_to_kafka(self, message) -> None:
        self.producer.send(self.producer_topic, value=message)
        self.producer.flush()
        logger.info("Message produced to Kafka!")

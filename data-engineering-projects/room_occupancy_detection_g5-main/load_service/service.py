import os

from base_logger import logger
from kafka import KafkaConsumer
from pymongo import MongoClient


class LoadService:
    def __init__(self):
        self.kafka_server = os.environ.get("KAFKA_SERVER")
        self.kafka_topic = os.environ.get("KAFKA_TOPIC")
        self.mongodb_connection_url = os.environ.get("MONGODB_CONNECTION_URL")
        self.db_name = os.environ.get("MONGODB_DATABASE")
        self.collection_name = os.environ.get("MONGODB_COLLECTION")

        if None in (
            self.kafka_server,
            self.kafka_topic,
            self.mongodb_connection_url,
            self.db_name,
            self.collection_name,
        ):
            error_msg = "You need to specify KAFKA_SERVER, KAFKA_TOPIC, MONGODB_CONNECTION_URL, MONGODB_DATABASE and MONGODB_COLLECTION"
            logger.error(error_msg)
            raise Exception(error_msg)

        self.client = MongoClient(host=self.mongodb_connection_url)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

        self.consumer = KafkaConsumer(
            self.kafka_topic,
            group_id="save-to-db",
            enable_auto_commit=False,
            auto_offset_reset="earliest",
            bootstrap_servers=self.kafka_server,
        )

    def save_data_to_db(self, message):
        self.collection.update_one(
            {"_id": message["timestamp"]},
            {
                "$set": {
                    message["room_id"]: {
                        "light_level": message["light_level"],
                        "humidity": message["humidity"],
                        "humidity_ratio": message["humidity_ratio"],
                        "co2": message["co2"],
                        "temperature_in_fahrenheit": message[
                            "temperature_in_fahrenheit"
                        ],
                        "temperature_in_celsius": message["temperature_in_celsius"],
                        "is_occupied": message["is_occupied"],
                    }
                }
            },
            upsert=True,
        )
        logger.info("Record saved to database!")

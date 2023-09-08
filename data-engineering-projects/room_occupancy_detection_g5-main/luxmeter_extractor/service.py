import datetime
import json
import logging
import os
import time

import requests
from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class ExtractorService:
    def __init__(self):
        self.luxmeter_endpoint = os.environ.get("LUXMETER_ENDPOINT")

        if None in (self.luxmeter_endpoint,):
            msg = "You need to specify LUXMETER_ENDPOINT"
            logger.error(msg)
            raise Exception(msg)

        self.rooms = ["kitchen", "bedroom", "bathroom", "living_room"]
        self.kafka_topic = os.environ.get("KAFKA_TOPIC")
        self.producer = KafkaProducer(
            bootstrap_servers=os.environ.get("KAFKA_SERVER"),
            acks=1,
            value_serializer=lambda v: json.dumps(v, default=str).encode("ascii"),
        )

    def get_luxmeter_data(self):
        for room in self.rooms:
            requested_url = f"{self.luxmeter_endpoint}/{room}"
            retries_count = 0
            while True:
                api_response = self.make_get_request(requested_url)
                if api_response:
                    # extract last/recent record
                    recent_record = api_response["measurements"][-1]
                    recent_timestamp = recent_record["timestamp"]
                    # check to see if it is the recent timestamp
                    if (
                        recent_timestamp
                        == datetime.datetime.now()
                        .replace(second=0, microsecond=0)
                        .isoformat()
                    ):
                        luxmeter_data = {"room_id": room, "measurements": recent_record}
                        logger.info(f"Received Luxmeter Data: {luxmeter_data}")
                        self.producer.send(topic=self.kafka_topic, value=luxmeter_data)
                        self.producer.flush()
                        break
                if retries_count > 10:
                    error_msg = "Could not get recent data from api"
                    logging.error(error_msg)
                    raise Exception(error_msg)
                time.sleep(1)
                retries_count += 1

    def make_get_request(self, url: str):
        retries_count = 0
        while True:
            try:
                response = requests.get(url)
                if response.ok:
                    return response.json()
                else:
                    logger.warning(
                        f"Got status code {response.status_code} against {url}"
                    )
                    return response
            except requests.exceptions.ConnectionError as e:
                if retries_count > 10:
                    error_msg = "Could not connect to the api"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                time.sleep(1)
                retries_count += 1

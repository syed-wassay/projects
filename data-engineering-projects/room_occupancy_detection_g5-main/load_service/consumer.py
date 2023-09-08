from json import loads

from base_logger import logger
from service import LoadService

load_service = LoadService()

for message in load_service.consumer:
    message = message.value
    data = loads(message.decode("utf-8"))
    logger.info(f"Received Data: {data}")
    load_service.save_data_to_db(data)

    # commit message after loading to db
    load_service.consumer.commit()

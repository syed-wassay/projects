import numpy as np
from base_logger import logger
from service import PredictionService

# initialize service
prediction_service = PredictionService()

for message in prediction_service.consumer:
    message = message.value
    logger.info(f"Received Transformed/Merged Data: {message}")

    # getting room_id
    room_id = message.get("room_id")
    if not room_id:
        logger.warning("Could not find room_id in consumed data!")
        continue

    # getting required features for getting predictions from ml model
    temperature = message["temperature_in_celsius"]
    humidity = message["humidity"]
    light = message["light_level"]
    co2 = message["co2"]
    humidity_ratio = message["humidity_ratio"]

    # create 2D array as input to model
    X = np.array([temperature, humidity, light, co2, humidity_ratio])
    X = X.reshape(1, -1)

    # feed data to model and get prediction
    prediction = prediction_service.get_prediction(X)

    # set occupied as True against 1 and False against 0
    occupancy = bool(prediction)

    # update message to be produced in a separate kafka topic
    message["is_occupied"] = occupancy
    logger.info(f'Room: {message["room_id"]} | Predicted Occupancy: {occupancy}')

    # send message to kafka producer
    prediction_service.send_to_kafka(message)

    # commit offset after saving the prediction
    prediction_service.consumer.commit()

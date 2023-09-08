## prediction-service

### Purpose
This service was created to apply predictions in real-time on the data coming from kafka after being transformed and merged. The service loads model from provided `pickle file` and saves prediction to the given kafka topic.

### Depends-on
* broker

### Requirements
The service requires following `ENV VARIABLES`

`KAFKA_SERVER` (kafka hostname/ip with port)

`CONSUMER_TOPIC` (topic name to consume merged data from)

`PRODUCER_TOPIC` (topic name to produce data into)

`MODEL_FILENAME` (filename of exported model / pickle filename)

### Running the service
You can use `python3` or `docker` to run the service. You will find `requirements.txt` and a `Dockerfile` as well inside the service directory

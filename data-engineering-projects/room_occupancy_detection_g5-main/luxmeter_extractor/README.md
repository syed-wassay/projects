## luxmeter-extractor

### Purpose
This service was created to fetch data from REST endpoint exposed by the sensorsmock service. the service requests luxmeter data from the endpoint given in real-time and produces the received data into a kafka topic.

### Depends-on
* sensorsmock
* broker

### Requirements
The service requires following `ENV VARIABLES`

`KAFKA_SERVER` (kafka hostname/ip with port)

`KAFKA_TOPIC` (output topic name)

`LUXMETER_ENDPOINT` (endpoint of luxmeter)

### Running the service
You can use `python3` or `docker` to run the service. You will find `requirements.txt` and a `Dockerfile` as well inside the service directory

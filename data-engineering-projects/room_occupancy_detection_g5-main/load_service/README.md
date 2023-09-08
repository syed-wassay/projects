## load-service

### Purpose
This service was created to load data in real-time into a `mongodb` database which can be consumed by the frontend service. The service consumes data from specified kafka-topic and loads that data into a specified `mongodb` collection. 

### Depends-on
* broker

### Requirements
The service requires following `ENV VARIABLES`

`KAFKA_SERVER` (kafka hostname/ip with port)

`KAFKA_TOPIC` (topic name to consume data from)

`MONGODB_CONNECTION_URL` (connection uri/url of the mongodb database)

`MONGODB_DATABASE` (name of database to write data to)

`MONGODB_COLLECTION` (name of collection to store data into)

### Running the service
You can use `python3` or `docker` to run the service. You will find `requirements.txt` and a `Dockerfile` as well inside the service directory

## transformation-service

### Purpose
This service was created to read streams of 4 senors data and merge them to be able to apply predictions later on. The service uses `pyspark` to read stream from kafka and after applying transformation and merging, it produces data into a kafka topic which can be consumed by other service(s).

### Depends-on
* broker

### Requirements
The service requires following `ENV VARIABLES`

`KAFKA_SERVER` (kafka hostname/ip with port)

`CARBON_SENSE_TOPIC` (topic name to read carbon-sense data from)

`MOISTURE_MATE_TOPIC` (topic name to read moisture-mate data from)

`LUXMETER_TOPIC` (topic name to read luxmeter data from)

`SMART_THERMO_TOPIC` (topic name to read smart-thermo data from)

`OUTPUT_TOPIC` (topic name where merged data will be produced)

### Running the service
You will need `docker` to run the service. You will find the `Dockerfile` inside the service directory

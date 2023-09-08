#!/bin/bash

# create directory to store s3 data
mkdir -p ./s3_data

# create directory for s3-connector
mkdir -p ./s3_connector

# export ENV variables from .env file
export $(cat .env)

# use envsubst to replace ENV variables in s3-connector-config.json
# copy file with replaced values inside s3_connector
envsubst < s3-connector-config.json > s3_connector/s3-connector-config.json

# stop and remove if containers are already running
docker compose --profile data_persistence_layer \
        --profile data_source \
        --profile data_transport_layer \
        --profile data_transformation_layer \
        --profile data_prediction_layer \
        --profile data_load_layer \
        --profile frontend_layer \
        rm -svf 

# start only the services with profile=data_persistence_layer (all related to kafka)
docker compose --profile data_persistence_layer up --remove-orphans --build -d

# sleep for 30 seconds for broker to be up and running
sleep 30

# start remaining services
docker compose --profile data_source \
        --profile data_transport_layer \
        --profile data_transformation_layer \
        --profile data_prediction_layer \
        --profile data_load_layer \
        --profile frontend_layer \
        up --remove-orphans --build -d
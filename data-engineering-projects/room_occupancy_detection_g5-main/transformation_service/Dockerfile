FROM bitnami/spark:3.3.1 

USER root

WORKDIR /app

COPY main.py main.py

CMD spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 main.py

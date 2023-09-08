import logging
import os

import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import SparkSession

# create logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class TransformationService:
    def __init__(self):
        self.kafka_server = os.environ.get("KAFKA_SERVER")
        self.carbon_sense_topic = os.environ.get("CARBON_SENSE_TOPIC")
        self.moisture_mate_topic = os.environ.get("MOISTURE_MATE_TOPIC")
        self.luxmeter_topic = os.environ.get("LUXMETER_TOPIC")
        self.smart_thermo_topic = os.environ.get("SMART_THERMO_TOPIC")
        self.output_topic = os.environ.get("OUTPUT_TOPIC")

        if None in (
            self.kafka_server,
            self.carbon_sense_topic,
            self.moisture_mate_topic,
            self.luxmeter_topic,
            self.smart_thermo_topic,
            self.output_topic,
        ):
            error_msg = "You need to specify KAFKA_SERVER, CARBON_SENSE_TOPIC, MOISTURE_MATE_TOPIC, LUXMETER_TOPIC, SMART_THERMO_TOPIC and OUTPUT_TOPIC"
            logger.error(error_msg)
            raise Exception(error_msg)

    def read_stream_from_kafka(self, kafka_topic):
        stream_reader = (
            spark.readStream.format("kafka")
            .option("kafka.bootstrap.servers", self.kafka_server)
            .option("subscribe", kafka_topic)
            .load()
        )
        return stream_reader

    def unpack_json_message_using_schema(self, df, schema):
        df = df.select(F.col("value").cast(T.StringType()))
        df = df.select(F.from_json(df.value, schema).alias("data"))
        df = df.select("data.*")
        return df


# create spark session
spark = (
    SparkSession.builder.master("local[*]")
    .appName("TransformService")
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1")
    .getOrCreate()
)

# create instance of service
transformation_service = TransformationService()

# read streams for all 4 sensors
carbon_sense_df = transformation_service.read_stream_from_kafka(
    transformation_service.carbon_sense_topic
)

moisture_mate_df = transformation_service.read_stream_from_kafka(
    transformation_service.moisture_mate_topic
)

luxmeter_df = transformation_service.read_stream_from_kafka(
    transformation_service.luxmeter_topic
)

smart_thermo_df = transformation_service.read_stream_from_kafka(
    transformation_service.smart_thermo_topic
)

# Define schemas for each sensor
carbon_sense_schema = T.StructType(
    [
        T.StructField("room_id", T.StringType()),
        T.StructField("timestamp", T.StringType()),
        T.StructField("co2", T.FloatType()),
    ]
)

moisture_mate_schema = T.StructType(
    [
        T.StructField("room_id", T.StringType()),
        T.StructField("timestamp", T.StringType()),
        T.StructField("humidity", T.FloatType()),
        T.StructField("humidity_ratio", T.FloatType()),
    ]
)

luxmeter_schema = T.StructType(
    [
        T.StructField("room_id", T.StringType()),
        T.StructField(
            "measurements",
            T.StructType(
                [
                    T.StructField("timestamp", T.StringType()),
                    T.StructField("light_level", T.FloatType()),
                ]
            ),
        ),
    ]
)

smart_thermo_schema = T.StructType([T.StructField("column1", T.StringType())])

# load streams
carbon_sense_df = transformation_service.unpack_json_message_using_schema(
    carbon_sense_df, carbon_sense_schema
)

moisture_mate_df = transformation_service.unpack_json_message_using_schema(
    moisture_mate_df, moisture_mate_schema
)

luxmeter_df = transformation_service.unpack_json_message_using_schema(
    luxmeter_df, luxmeter_schema
)
luxmeter_df = luxmeter_df.select(["room_id", "measurements.*"])

smart_thermo_df = transformation_service.unpack_json_message_using_schema(
    smart_thermo_df, smart_thermo_schema
)

splitted_col = F.split(smart_thermo_df["column1"], ",")
smart_thermo_df = (
    smart_thermo_df.withColumn("timestamp", splitted_col.getItem(1))
    .withColumn("room_id", splitted_col.getItem(2))
    .withColumn("temperature_in_fahrenheit", splitted_col.getItem(3))
)

smart_thermo_df = smart_thermo_df.drop("column1")
smart_thermo_df = smart_thermo_df.withColumn(
    "temperature_in_fahrenheit",
    smart_thermo_df["temperature_in_fahrenheit"].cast("double"),
)
smart_thermo_df = smart_thermo_df.withColumn(
    "timestamp", smart_thermo_df["timestamp"].cast("timestamp")
)

# convert temperature from F into C
smart_thermo_df = smart_thermo_df.withColumn(
    "temperature_in_celsius",
    (smart_thermo_df["temperature_in_fahrenheit"] - 32) * (5 / 9),
)

# merge data
merged_df = (
    carbon_sense_df.join(moisture_mate_df, ["timestamp", "room_id"])
    .join(luxmeter_df, ["timestamp", "room_id"])
    .join(smart_thermo_df, ["timestamp", "room_id"])
)

# for confirmation
merged_df.printSchema()

# pack data to be able to stream into kafka topic
packed_for_streaming_into_kafka = merged_df.withColumn(
    "data_packed_for_kafka", F.to_json(F.struct(*merged_df.columns))
).select(F.col("data_packed_for_kafka").alias("value"))

# send to kafka topic
packed_for_streaming_into_kafka.writeStream.format("kafka").option(
    "kafka.bootstrap.servers", transformation_service.kafka_server
).option("topic", transformation_service.output_topic).option(
    "checkpointLocation",
    os.path.join("checkpoints", transformation_service.output_topic),
).start().awaitTermination()

spark.stop()

import json
import time
import requests
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, lit, pandas_udf, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, BooleanType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaToAzurePostgresWithPrediction") \
    .config("spark.jars.packages", 
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5,"
            "org.postgresql:postgresql:42.7.5") \
    .getOrCreate()

_ = spark.range(1).count()

# Kafka config
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "<your_kafka_topic>"
ENDPOINT_URL = "http://343ae727-f835-45f0-a8e3-16e6f2bb1a08.centralindia.azurecontainer.io/score"

# Define schema
schema = StructType([
    StructField("transaction_id", IntegerType(), True),
    StructField("user_id", IntegerType(), True),
    StructField("amount", FloatType(), True),
    StructField("transaction_type", StringType(), True),
    StructField("status", StringType(), True),
    StructField("device_id", StringType(), True),
    StructField("location", StringType(), True),
    StructField("is_foreign_transaction", BooleanType(), True),
    StructField("num_chargebacks", IntegerType(), True)
])

# Read stream from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON payload
df = df.selectExpr("CAST(value AS STRING)") \
       .select(from_json(col("value"), schema).alias("data")) \
       .select("data.*")

# Fraud prediction UDF
@pandas_udf("integer")
def predict_fraud_udf(
    transaction_id: pd.Series, user_id: pd.Series, amount: pd.Series,
    transaction_type: pd.Series, status: pd.Series, device_id: pd.Series,
    location: pd.Series, is_foreign_transaction: pd.Series, num_chargebacks: pd.Series
) -> pd.Series:

    # Encode categorical values with complete mapping + fallback
    transaction_type_num = transaction_type.replace({
        "withdrawal": 0,
        "transfer": 1,
        "payment": 2,
        "purchase": 3
    }).fillna(4)

    status_num = status.replace({
        "completed": 0,
        "pending": 1,
        "failed": 2,
        "success": 3
    }).fillna(4)

    device_flag = device_id.apply(lambda x: 1 if str(x).startswith("devF") else 0)
    foreign_flag = location.apply(lambda x: 1 if "India" not in str(x) else 0)

    # Assemble features for prediction
    features = pd.concat([
        user_id, amount,
        transaction_type_num, status_num,
        device_flag, foreign_flag,
        is_foreign_transaction.astype(int), num_chargebacks
    ], axis=1).values.tolist()

    for attempt in range(3):
        try:
            response = requests.post(
                ENDPOINT_URL,
                headers={"Content-Type": "application/json"},
                data=json.dumps({"data": features}),
                timeout=5
            )
            response.raise_for_status()

            # Parse the raw response
            print("Raw response text:", response.text)

            # Handles both cases: response as JSON string or JSON object
            parsed = json.loads(response.text)
            result = parsed if isinstance(parsed, dict) else json.loads(parsed)

            if "result" in result:
                return pd.Series(result["result"])
            else:
                print("Unexpected format from endpoint:", result)

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)

    print("All retries failed. Returning 0s as fallback predictions.")
    return pd.Series([0] * len(user_id))




# Add prediction and potential fraud logic
df_with_pred = df.withColumn("predicted_fraud", predict_fraud_udf(
    col("transaction_id"), col("user_id"), col("amount"),
    col("transaction_type"), col("status"), col("device_id"),
    col("location"), col("is_foreign_transaction"), col("num_chargebacks")
)).withColumn(
    "potential_fraud", 
    when(
        (col("amount") > 5000) & 
        (col("is_foreign_transaction") == True) & 
        (col("num_chargebacks") > 2),
        1
    ).otherwise(0)
)

# Write to Azure PostgreSQL
def write_to_postgres(batch_df, batch_id):
    print(f" Processing batch: {batch_id}")
    try:
        batch_df.select(
            "transaction_id", "user_id", "amount", "transaction_type",
            "status", "device_id", "location", "is_foreign_transaction",
            "num_chargebacks", "potential_fraud", "predicted_fraud"  
        ).write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://<azure-host>.postgres.database.azure.com:5432/fraud_detection_db") \
            .option("dbtable", "<postgres-table>") \
            .option("user", "<user-name>") \
            .option("password", "<password>") \
            .option("sslmode", "require") \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()
        print("Predictions saved to '<your_db>' table!")
    except Exception as e:
        print("Error writing to PostgreSQL:", e)

# Start streaming
df_with_pred.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .start() \
    .awaitTermination()

from kafka import KafkaConsumer
from pymongo import MongoClient
import json
from key import MONGO_URI

# Kafka Configuration
KAFKA_BROKER = 'kafka:9093'  # Match the Kafka advertised listener in docker-compose.yml
TOPIC = 'news'

# MongoDB Configuration
DB_NAME = 'bigdata'
COLLECTION_NAME = 'project'

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

# Create Kafka Consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',  # Start consuming from the earliest message
    enable_auto_commit=True,
    group_id='news-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print(f"Listening to Kafka topic: {TOPIC}")

try:
    for message in consumer:
        # Process each message
        data = message.value  # Message value is a dictionary
        print(f"Received message: {data}")

        # Insert the message into MongoDB
        collection.insert_one(data)
        print(f"Inserted message into MongoDB: {data}")

except Exception as e:
    print(f"Error in consumer: {e}")
finally:
    consumer.close()
    mongo_client.close()
    print("Consumer shut down.")
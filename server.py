from confluent_kafka import Consumer
from pymongo import MongoClient
import json
from key import MONGO_URI

#Docker implementation
#server:
  #  build:
  #    context: .
  #    dockerfile: Dockerfile.server
  #  container_name: server
  #  depends_on:
  #    - kafka
  #    - mongodb

# Kafka Configuration
# working with localhost, having issues with docker -> use kafka:9092
KAFKA_BROKER = 'kafka:9092'  # Update this if Kafka is running elsewhere
TOPIC = 'news'

# MongoDB Configuration
DB_NAME = 'bigdata'
COLLECTION_NAME = 'project'

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

# Create Kafka Consumer
consumer_config = {
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'  # Start from the beginning of the topic
}

consumer = Consumer(consumer_config)
consumer.subscribe([TOPIC])

print(f"Server is up and listening to Kafka topic: {TOPIC}")

try:
    while True:
        msg = consumer.poll(1.0)  # Poll for messages with a 1-second timeout
        if msg is None:
            continue  # No message received
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        
        # Deserialize JSON blob
        try:
            data_blob = json.loads(msg.value().decode('utf-8'))
        except Exception as e:
            print(f"Error decoding message: {e}")
            continue

        # Process each JSON object in the blob
        for record in data_blob:
            # Extract relevant fields
            relevant_data = {
                "id": record.get("id"),
                "message": record.get("message"),
                "timestamp": record.get("timestamp", None)
            }

            # Insert into MongoDB
            collection.insert_one(relevant_data)

        print(f"Processed {len(data_blob)} records and saved to MongoDB.")

except KeyboardInterrupt:
    print("Server shut down by user.")
except Exception as e:
    print(f"Error in server: {e}")
finally:
    consumer.close()
    mongo_client.close()

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

# Create a topic in docker
# docker exec -it kafka kafka-topics --create --topic news --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
# No longer need to include the above, added to docker file

# Kafka Configuration
# working with localhost, having issues with docker -> use kafka:9092

# Notes:
# 1) There is a networking issue happening in the way kafka is referenced, it may have to do with the
#       ports/listeners/activeListeners configs, keep working on that
# 2) Everything works as expected when the server is removed from the docker-compose image, if it uses localhost
#       it can connect, same as the producer1 script
# 3) This current implementation of the docker-compose file lets kafka startup uninterrupted and creates the news topic
#       which is a good step in the right direction

# todo:
# 1) further debugging of connection issue stated above
# 2) add the two other producer scripts
# 3) add the query params and api endpoints for data gathering (easy)


# MongoDB Configuration
DB_NAME = 'bigdata'
COLLECTION_NAME = 'project'

# Connect to MongoDB
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]


KAFKA_BROKER = 'kafka:9092'  # Update this if Kafka is running elsewhere
TOPIC = 'news'

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

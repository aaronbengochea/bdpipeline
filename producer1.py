from confluent_kafka import Producer
import json

# Kafka Configuration
KAFKA_BROKER = 'localhost:9092'  # Update if Kafka is running elsewhere
TOPIC = 'news'

# Create Kafka Producer
producer_config = {
    'bootstrap.servers': KAFKA_BROKER
}
producer = Producer(producer_config)

def delivery_report(err, msg):
    """Callback for delivery reports."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Create and send a JSON blob
data_blob = [
    {"id": 1, "message": "Hello, Kafka!", "timestamp": "2024-12-08T12:00:00Z"},
    {"id": 2, "message": "This is a test message", "timestamp": "2024-12-08T12:01:00Z"}
]

try:
    # Serialize JSON blob and send to Kafka
    producer.produce(
        TOPIC,
        key=None,
        value=json.dumps(data_blob).encode('utf-8'),
        callback=delivery_report
    )
    producer.flush()  # Ensure all messages are sent
except Exception as e:
    print(f"Error producing message: {e}")
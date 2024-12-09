from kafka import KafkaProducer
import json

# Kafka Configuration
KAFKA_BROKER = 'localhost:9093'  # Host access to Kafka
TOPIC = 'news'

# Create Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Message to send
message = {
    "id": 1,
    "message": "This is a test message",
    "timestamp": "2024-12-09T12:00:00Z"
}

try:
    # Send the message
    producer.send(TOPIC, value=message)
    producer.flush()
    print(f"Sent message: {message}")
except Exception as e:
    print(f"Error producing message: {e}")
finally:
    producer.close()
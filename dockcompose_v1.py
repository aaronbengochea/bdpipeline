"""
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    networks: 
      - app-network

  kafka:
    image: confluentinc/cp-kafka:latest
    container_name: kafka
    ports:
      - "9092:9092"
      - "9093:9093"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    depends_on:
      - zookeeper
    networks: 
      - app-network

  kafka-init:
    image: confluentinc/cp-kafka:latest
    container_name: kafka-init
    depends_on:
      - kafka
    entrypoint: >
      sh -c "
      sleep 10 &&
      kafka-topics --bootstrap-server kafka:9092 --create --topic news --partitions 1 --replication-factor 1 &&
      echo 'Kafka topic news created successfully'
      "
    networks: 
      - app-network


  server-py:
    build: 
      dockerfile: Dockerfile.server
    container_name: server-py
    depends_on:
      - kafka
      - mongodb
    networks: 
      - app-network
    

  mongodb:
    image: mongo:latest
    container_name: mongodb
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
    networks: 
      - app-network

networks:
  app-network:

volumes:
  mongo-data:
"""
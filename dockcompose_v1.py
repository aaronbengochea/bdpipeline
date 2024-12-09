"""
version: '3.8'
services:
  kafka:
    image: wurstmeister/kafka:latest
    environment:
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9093
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9093
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
    ports:
      - "9093:9093"
    networks:
      - kafka-net
    depends_on:
      - zookeeper

  zookeeper:
    image: wurstmeister/zookeeper:latest
    ports:
      - "2181:2181"
    networks:
      - kafka-net

  python-consumer:
    build: .
    depends_on:
      - kafka
    environment:
      KAFKA_SERVER: kafka:9093
    networks:
      - kafka-net

  mongodb:
    image: mongo:latest
    container_name: mongodb
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
    networks: 
      - kafka-net

networks:
  kafka-net:
    driver: bridge

volumes:
  mongo-data:

"""
# https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html

from confluent_kafka import Producer
from dotenv import load_dotenv
import json
import os

# load .env
load_dotenv()

# Configure the Kafka producer
conf = {
        'bootstrap.servers': os.getenv('KAFKA_BROKER'),  # Broker address
        'client.id': 'python-producer',
        'delivery.timeout.ms': 5000
    }

# Callback function to handle delivery reports
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def produce_data(topic: str, data: dict):
    """
    Send data to the broker
    Args:
        data (dict): data to send
    """
    # Create a Kafka producer with the given configuration
    producer = Producer(conf)

    # Send the JSON data to the Kafka topic
    producer.produce(topic=topic, value=json.dumps(data), on_delivery=delivery_report)
    producer.poll(0) # wait callback message

    # Wait for any outstanding messages to be delivered and delivery reports to be received
    producer.flush()



### other:
# with open('data.json', 'w') as json_file:
#     json.dump(feed, json_file, indent=4)

# with open('data.json', 'r') as json_file:
#     data = json.load(json_file)

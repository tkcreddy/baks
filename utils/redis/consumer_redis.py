import redis


def redis_consumer():
    # Connect to Redis
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

    topic = 'my_topic'  # Define the topic (channel)
    print(f"Consumer is subscribed to topic: {topic}")

    # Subscribe to the topic
    pubsub = redis_client.pubsub()
    pubsub.subscribe(topic)

    print("Listening for messages...")
    for message in pubsub.listen():
        if message and message['type'] == 'message':  # Check for valid messages
            print(f"Received: {message['data']}")


if __name__ == "__main__":
    redis_consumer()

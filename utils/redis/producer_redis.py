import redis
import time


def redis_producer():
    # Connect to Redis
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

    topic = 'my_topic'  # Define the topic (channel)
    print(f"Producer is publishing messages to topic: {topic}")

    # Publish messages
    for i in range(1, 6):
        message = f"Message {i}"
        redis_client.publish(topic, message)
        print(f"Published: {message}")
        time.sleep(1)  # Simulate delay between messages


if __name__ == "__main__":
    redis_producer()

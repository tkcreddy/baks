import redis
from redis_om import HashModel
from dataclasses import dataclass

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

class URLMapping(HashModel):
    """Redis-OM HashModel for URL Mapping"""
    short_code: str
    original_url: str

    class Meta:
        database = redis_client  # Connects to Redis

    def save_to_hashmap(self):
        """Save the mapping into a specific Redis hash map."""
        hash_name = f"url_mapping"
        redis_client.hset(hash_name, mapping={"short_code": self.short_code, "original_url": self.original_url})
        return self.short_code

    @classmethod
    def get_from_hashmap(cls, short_code: str):
        """Retrieve data from a specific Redis hash map."""
        hash_name = f"url_mapping"
        data = redis_client.hgetall(hash_name)
        if data:
            return cls(**data)  # Convert Redis hash back to a URLMapping instance
        return None

# Example: Save a URL mapping
mapping = URLMapping(short_code="abc123", original_url="https://example.com")
mapping.save_to_hashmap()  # Save to specific hash map

# Example: Retrieve the mapping from Redis
retrieved_mapping = URLMapping.get_from_hashmap("abc123")
if retrieved_mapping:
    print(f"Retrieved URL: {retrieved_mapping.original_url}")
else:
    print("No data found")

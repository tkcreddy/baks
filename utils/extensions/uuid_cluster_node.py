import uuid
import hashlib
import base64
from utils.ReadConfig import ReadConfig as rc
def generate_uuid_with_key(key):
    # Use SHA-256 hash function
    hash_object = hashlib.sha256(key.encode())
    hashed_key = hash_object.digest()

    # Encode the hashed key to base64
    base64_encoded = base64.b64encode(hashed_key).decode('utf-8')

    # Create a UUID-like alphanumeric string
    generated_uuid = base64_encoded[:-2]  # Trim '==' from the end

    return generated_uuid

# if __name__ == "__main__":
#     key = "your_key_here"
#     generated_uuid = generate_uuid_with_key(key)
#
#     print(f"Generated UUID-like string for key '{key}': {generated_uuid}")


if __name__ == "__main__":
    read_config = rc("/Users/krishnareddy/PycharmProjects/kobraCldSS")
    #key = "your_key_here"
    key_read =  read_config.encryption_config
    key = key_read['key']
    generated_uuid = generate_uuid_with_key(key)

    print(f"Generated UUID for key '{key}': {generated_uuid}")

import uuid
import base64
import time
import re

def generate_time_based_uid():
    # Get current timestamp
    current_time = int(time.time() * 1000)  # Convert to milliseconds

    # Create a UUID using the timestamp
    uid = uuid.uuid5(uuid.NAMESPACE_DNS, str(current_time))

    # Encode the UID to base64
    base64_encoded = base64.urlsafe_b64encode(uid.bytes).decode('utf-8')

    # Remove padding characters
    base64_encoded = base64_encoded.rstrip("=")
    base64_encoded = re.sub("-", "_", base64_encoded)

    return base64_encoded

if __name__ == "__main__":
    generated_uid = generate_time_based_uid()

    print(f"Generated time-based UID: {generated_uid}")

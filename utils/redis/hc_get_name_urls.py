import redis
import ast  # For safely converting strings back to dictionaries

REDIS_HASH_NAME = 'url_to_cluster'


def get_urls_with_cluster(hash_name: str, redis_host: str = 'localhost', redis_port: int = 6379,
                          redis_db: int = 0) -> dict:
    """
    Retrieve data from a Redis hash where 'age' matches the target_age.

    :param redis_hash_name: Name of the Redis hash.
    :param target_age: The age value to filter rows.
    :param redis_host: Redis server host.
    :param redis_port: Redis server port.
    :param redis_db: Redis database number.
    :return: List of matching rows.
    """
    # Connect to Redis
    r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

    matching_rows = {}
    try:
        # Get all fields and values from the hash
        all_data = r.hgetall(hash_name)
        url_list = []
        for field, value in all_data.items():
            # Convert the stored string back to a dictionary
            row = ast.literal_eval(value.decode('utf-8'))
            matching_rows[row.get('cluster_name')]=row['url']
            #
            # # Check if the 'age' key matches the target_age
            # if row.get('cluster_name') == cluster_name:
            #     # for value in row:
            #     #     url_list.append(value)
            #     matching_rows.append(row['url'])

    except Exception as e:
        print(f"Error: {e}")

    return matching_rows

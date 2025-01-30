import redis

class HcTrack:

    def __init__(self, host='localhost', port=6379,db=1):
        # Connect to Redis
        self.redis_client = redis.StrictRedis(host=host, port=port,db=db, decode_responses=True)


    def track_consecutive_failures(self, key:str,status:str,time:int=60,cluster_name:str =None):
        failure_count_key = f"{key}:::failure_count"

    # Get the latest health check result (e.g., pushed by an external service)
    #health_status = redis_client.get(key)  # Assume 'key' stores "pass" or "fail"

        if status == "healthy":
            print("Health check passed.")
            self.redis_client.set(failure_count_key, 0)  # Reset failure count on success
        elif status == "unhealthy":
            # Increment failure count on failure
            current_count = self.redis_client.incr(failure_count_key)
            print(f"Health check failed. Consecutive failures: {current_count}")
        self.redis_client.expire(failure_count_key,60)

    def lb_update(self, url:str,status:str,time:int=60,cluster_name:str =None):
        failure_count_key = f"{url}:::failure_count"

    # Get the latest health check result (e.g., pushed by an external service)
    #health_status = redis_client.get(key)  # Assume 'key' stores "pass" or "fail"

        if status == "healthy":
            print("Health check passed.")
            self.redis_client.set(failure_count_key, 0)  # Reset failure count on success
        elif status == "unhealthy":
            # Increment failure count on failure
            current_count = self.redis_client.incr(failure_count_key)
            print(f"Health check failed. Consecutive failures: {current_count}")
        self.redis_client.expire(failure_count_key,60)


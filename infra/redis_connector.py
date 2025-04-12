# In infra/redis_connector.py
import redis
import os

class RedisConnector:
    def __init__(self):
        redis_url = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
        self.client = None
        try:
            print(f"Attempting to connect to Redis at {redis_url}...")
            # decode_responses=True makes it return strings instead of bytes
            self.client = redis.Redis.from_url(redis_url, decode_responses=True)
            self.client.ping() # Check connection
            print("Redis connection successful.")
        except redis.exceptions.ConnectionError as e:
            print(f"Could not connect to Redis: {e}")
            self.client = None # Ensure client is None if connection failed
            # Depending on how critical Redis is, you might raise an error
            # raise ConnectionError(f"Failed to connect to Redis at {redis_url}") from e
        except Exception as e:
            print(f"An unexpected error occurred during Redis connection: {e}")
            self.client = None
            # raise ConnectionError(f"An error occurred during Redis connection at {redis_url}") from e

    def check_if_exists(self, set_key, item_id):
        """Checks if an item_id exists in the specified Redis set."""
        if self.client and item_id:
            try:
                return self.client.sismember(set_key, item_id)
            except Exception as e:
                print(f"Error checking Redis set {set_key}: {e}")
                return False # Fail safe: assume not exists on error
        return False

    def add_item(self, set_key, item_id):
        """Adds an item_id to the specified Redis set."""
        if self.client and item_id:
            try:
                return self.client.sadd(set_key, item_id)
            except Exception as e:
                print(f"Error adding to Redis set {set_key}: {e}")
                return 0 # Indicate failure
        return 0

    def close_connection(self):
        if self.client:
            self.client.close()
            print("Redis connection closed.")
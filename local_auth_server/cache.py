import redis
import json

class RedisCache:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)

    def get_cached_data(self, api_key: str):
        data = self.redis_client.get(api_key)
        if data:
            return json.loads(data)
        return None

    def set_cached_data(self, api_key: str, data: dict, ttl=1800):
        self.redis_client.setex(api_key, ttl, json.dumps(data))

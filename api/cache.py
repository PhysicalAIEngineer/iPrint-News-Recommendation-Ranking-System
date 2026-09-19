import json
import os

import redis

_client = redis.Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=True,
)


def get_cached(key):
    try:
        value = _client.get(key)
        return json.loads(value) if value else None
    except redis.RedisError:
        return None


def set_cached(key, value, ttl_seconds=300):
    try:
        _client.setex(key, ttl_seconds, json.dumps(value))
    except redis.RedisError:
        pass

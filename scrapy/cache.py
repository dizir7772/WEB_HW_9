import redis
from redis_lru import RedisLRU


client = redis.StrictRedis(host="localhost", port=6379, password=None, db=3)
cache = RedisLRU(client)
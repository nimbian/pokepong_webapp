import redis
from pokepong.config import _cfg

r = redis.StrictRedis.from_url(_cfg('redis-connection'))

from flask import current_app
import redis

r = redis.StrictRedis.from_url(current_app.config['REDIS_CONNECTION'])

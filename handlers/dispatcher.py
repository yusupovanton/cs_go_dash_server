from handlers.imports import *
from handlers.config import *

'''REDIS'''

r = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    charset="utf-8",
    decode_responses=True,
    password=REDIS_PASS
)

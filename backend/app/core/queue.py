from rq import Queue
from app.core.redis import redis_conn

default_queue = Queue("default", connection=redis_conn)

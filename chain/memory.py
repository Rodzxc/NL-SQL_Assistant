from langgraph.checkpoint.redis import RedisSaver
from contextlib import contextmanager
from config import load_env
import os

# === Memoria persistente con redis-stack ===
@contextmanager
def memory_checkpointer():
    load_env()
    env_ = os.environ.get('ENV', 'development')

    # docker-compose
    if env_ == 'production': # ENV = 'production' --> DOCKER_REDIS_URI = redis://redis:6379, ver docker-compose
        REDIS_URI = os.environ['DOCKER_REDIS_URI']
    # Local
    else: # ENV = '' --> REDIS_URI = redis://localhost:6379
        REDIS_URI = os.environ['REDIS_URI']
    
    with RedisSaver.from_conn_string(REDIS_URI) as checkpointer:
            yield checkpointer.setup()
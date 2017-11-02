from flask.ext.cache import Cache

from settings import CACHE_REDIS_HOST, CACHE_REDIS_PORT, CACHE_REDIS_PASSWORD, CACHE_SESSION_DB

session_cache = Cache(
    config={
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_HOST': CACHE_REDIS_HOST,
        'CACHE_REDIS_PORT': CACHE_REDIS_PORT,
        'CACHE_REDIS_PASSWORD': CACHE_REDIS_PASSWORD,
        'CACHE_REDIS_DB': CACHE_SESSION_DB
    }
)

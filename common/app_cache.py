from redis import Redis
import simplejson as json

from settings import CACHE_REDIS_HOST, CACHE_REDIS_PORT, CACHE_REDIS_PASSWORD, CACHE_SESSION_DB


class Cache(Redis):
    def __init__(self, host, port, db):
        self.host = host
        self.port = port
        self.db = db
        super(Cache, self).__init__(host=self.host, port=self.port, db=self.db)

    def get(self, key, **kwargs):
        data_format = kwargs.pop('format', 'str')
        value = super(Cache, self).get(key, **kwargs)
        if data_format == 'json':
            value = json.loads(value) if value else {}
        return value

    def set(self, key, value, **kwargs):
        data_format = kwargs.pop('format', 'str')
        if data_format == 'json':
            value = json.dumps(value)
        return super(Cache, self).set(key, value, **kwargs)

    def delete(self, *args):
        return super(Cache, self).delete(*args)


session_cache = Cache(CACHE_REDIS_HOST, CACHE_REDIS_PORT, CACHE_SESSION_DB)

from redis import Redis

class Cache:

  def __init__(self, prefix=''):
    self.prefix = 'cache:' + prefix
    self.redis = Redis(port=5102)


  def set(self, key, value):
    self.redis.set(self.prefix + str(key), value)


  def get(self, key):
    return self.redis.get(self.prefix + str(key))
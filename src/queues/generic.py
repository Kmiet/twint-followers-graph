from redis import Redis

# Changed to set not to duplicate the items
class Queue:

  def __init__(self, suffix=''):
    self.key = 'queue:' + suffix
    self.redis = Redis(port=5102)

  def deque(self):
    val = self.redis.spop(self.key)
    if val is None: 
      return None
      
    return val.decode('utf8')

  
  def enque(self, *item):
    self.redis.sadd(self.key, *item)

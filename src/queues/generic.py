from redis import Redis

class Queue:

  def __init__(self, suffix=''):
    self.key = 'queue:' + suffix
    self.redis = Redis(port=5102)

  def deque(self):
    return self.redis.rpop(self.key).decode('utf8')

  
  def enque(self, *msg):
    self.redis.lpush(self.key, *msg)

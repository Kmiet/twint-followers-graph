from .generic import Queue

# Changed to set not to duplicate the items
class TweetQueue(Queue):

  def __init__(self):
    super().__init__(suffix='tweet:')


  def deque(self):
    val = self.redis.rpop(self.key)
    if val is None: 
      return None
      
    return val.decode('utf8')

  
  def enque(self, items):
    self.redis.lpush(self.key, *items)
  

UserTweetsQueue = TweetQueue()

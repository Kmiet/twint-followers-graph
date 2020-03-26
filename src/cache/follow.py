from .generic import Cache

class FollowCache(Cache):
  
  def __init__(self):
    super().__init__(prefix='follow:')
    self.currently_processed_key = 'current:proc:cid:'
    self.processed_key = 'all:follow:processed'


  def get_currently_processed(self, cid=''):
    return self.get(self.currently_processed_key + str(cid))

  
  def set_currently_processed(self, uname, cid=''):
    self.set(self.currently_processed_key + str(cid), uname)

  
  def is_processed(self, uname):
    return self.redis.sismember(self.processed_key, uname)

  
  def set_processed(self, uname):
    self.redis.sadd(self.processed_key, uname)


UserFollowsCache = FollowCache()
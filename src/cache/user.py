from .generic import Cache

class UserCache(Cache):
  
  def __init__(self):
    super().__init__(prefix='user:')
    self.processed_key = 'all:processed:users'
    self.my_currently_processed_key = 'current:proc:cid:'
    self.counter_key = 'users_processed_counter'


  def get_currently_processed(self, cid=''):
    return self.get(self.my_currently_processed_key + str(cid))

  
  def set_currently_processed(self, uname, cid=''):
    self.set(self.my_currently_processed_key + str(cid), uname)

  
  def get_processed_count(self):
    count = self.redis.get(self.counter_key)
    return (int(count) if count is not None else 0)


  def increment_processed_count(self, uname):
    pipe = self.redis.pipeline()
    pipe.sadd(self.processed_key, uname)
    pipe.incr(self.counter_key)
    pipe.execute()

  
  def is_processed(self, uname):
    return self.redis.sismember(self.processed_key, uname)


UserDataCache = UserCache()
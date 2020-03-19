from .generic import Cache

class UserCache(Cache):
  
  def __init__(self):
    super().__init__(prefix='user:')
    self.currently_processed_key = 'currently:processed:user'
    self.counter_key = 'users_processed_counter'


  def get_currently_processed(self, cid=''):
    return self.get(self.currently_processed_key + str(cid))

  
  def set_currently_processed(self, id, cid=''):
    self.set(self.currently_processed_key + str(cid), id)

  
  def get_processed_count(self):
    count = self.redis.get(self.counter_key)
    return (int(count) if count is not None else 0)


  def increment_processed_count(self, id):
    pipe = self.redis.pipeline()
    pipe.set(self.prefix + str(id), 1)
    pipe.incr(self.counter_key)
    pipe.execute()


UserDataCache = UserCache()
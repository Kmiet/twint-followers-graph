from .generic import Cache

class FollowCache(Cache):
  
  def __init__(self):
    super().__init__(prefix='follow:')
    self.currently_processed_key = 'currently:processed:user'


  def get_currently_processed(self, cid=''):
    return self.get(self.currently_processed_key + str(cid))

  
  def set_currently_processed(self, sid, cid=''):
    self.set(self.currently_processed_key + str(cid), id)


UserFollowsCache = FollowCache()
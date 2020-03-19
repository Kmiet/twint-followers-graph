import sys
import time
sys.path.append("..")
import twint
from cache import UserDataCache
from queues import UserDataQueue, UserFollowsQueue
from repositories import User

USER_PROCESSED=1
CHECK_INTERVAL=2
MAX_PROCESSED_COUNT=150000

USER_OBJECT_FILTER_FIELDS = [ "url", "join_time", "is_private", "is_verified", "avatar", "background_image" ]

results = []

def __handle_twint_json(obj, config):
  global results
  result = obj.__dict__
  for field in USER_OBJECT_FILTER_FIELDS:
    del result[field]
  results.append(result)


class UserCollector:

  def __init__(self, collector_id=0):
    self.user_count = UserDataCache.get_processed_count()
    self.cid = collector_id
    self.c = twint.Config()
    self.c.Store_json = True
    self.c.User_full = True
    self.c.Output = "placeholder.json"
    self.c.Hide_output = True


  def run(self):
    username = UserDataCache.get_currently_processed(cid=self.cid)
    if username:
      self.__process_one(username)
    
    self.__process_all()

  
  def __process_all(self):
    while self.user_count < MAX_PROCESSED_COUNT:
      username = UserDataQueue.deque()

      if username is None:
        time.sleep(CHECK_INTERVAL)
      else:
        self.__process_one(username)

      self.user_count = UserDataCache.get_processed_count()


  def __process_one(self, username):
    global results
    UserDataCache.set_currently_processed(username, cid=self.cid)
    is_processed = UserDataCache.get(username) == USER_PROCESSED

    if is_processed:
      return

    self.c.Username = username
    twint.run.Lookup(self.c)

    User.update(results.pop())

    UserFollowsQueue.enque(username)
    UserDataCache.increment_processed_count(username)


sys.modules["twint.storage.write"].Json = __handle_twint_json
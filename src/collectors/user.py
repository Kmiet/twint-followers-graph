import sys
import time
sys.path.append("..")
import twint
import json
from cache import UserDataCache
from queues import UserDataQueue, UserFollowsQueue
from repositories import User

CHECK_INTERVAL=5
MAX_PROCESSED_COUNT=550000
MAX_FOLLOWING_ACCEPTED=3000

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
    # self.c = twint.Config()
    # self.c.Store_json = True
    # self.c.User_full = True
    # self.c.Output = "placeholder.json"
    # self.c.Hide_output = True


  def run(self):
    username = UserDataCache.get_currently_processed(cid=self.cid)
    if username:
      self.__process_one(username)
    
    self.__process_all()

  
  def __process_all(self):
    retries = 0
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

    if UserDataCache.is_processed(username):
      return

    done = False
    while not done:
      try:
        c = twint.Config()
        c.Store_json = True
        c.User_full = True
        c.Output = "placeholder.json"
        c.Hide_output = True
        c.Username = username
        twint.run.Lookup(c)
        done = True
      except:
        time.sleep(2)

    if results:
      result = results.pop()
      with open('../data/collector/users%s.dat' % self.cid, 'a+', 1) as f:
        f.write("%s\n" % json.dumps(result))

      # User.update(results.pop())

      if result['following'] < MAX_FOLLOWING_ACCEPTED:
        UserFollowsQueue.enque(username)
      UserDataCache.increment_processed_count(username)

# hacky
sys.modules["twint.storage.write"].Json = __handle_twint_json
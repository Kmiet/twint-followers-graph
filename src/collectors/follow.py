import sys
sys.path.append("..")
import twint
import time
from cache import UserFollowsCache
from queues import UserDataQueue, UserFollowsQueue
from repositories import Follow

MAX_RETRIES=100
CHECK_INTERVAL=2

results = []

def __handle_twint_json(obj, config):
  global results
  results.append(obj)


class FollowCollector:

  def __init__(self, collector_id=0):
    self.cid = collector_id
    self.c = twint.Config()
    self.c.Store_json = True
    self.c.User_full = False
    self.c.Output = "placeholder.json"
    self.c.Hide_output = True


  def run(self):
    username = UserFollowsCache.get_currently_processed(self.cid)
    if user_id:
      self.__process_one(username)
    
    self.__process_all()

  
  def __process_all(self):
    retries = 0
    while retries < MAX_RETRIES:
      username = UserFollowsQueue.deque()

      if not username:
        retries += 1
        time.sleep(CHECK_INTERVAL)
      else:
        retries = 0
        self.__process_one(username)


  def __process_one(self, username):
    global results
    UserFollowsCache.set_currently_processed(username, cid=self.cid)

    self.c.Username = username
    twint.run.Following(self.c)

    Follow.update_user_follows(username, results)
    UserDataQueue.enque(results)
    results.clear()


sys.modules["twint.storage.write"].Json = __handle_twint_json
import sys
sys.path.append("..")
import twint
import json
import time
from cache import UserFollowsCache
from queues import UserDataQueue, UserFollowsQueue
from repositories import Follow

MAX_RETRIES=1000
CHECK_INTERVAL=2

results = []

def __handle_twint_csv(obj, config):
  global results
  results.append(obj)


class FollowCollector:

  def __init__(self, collector_id=0):
    self.cid = collector_id


  def run(self):
    username = UserFollowsCache.get_currently_processed(self.cid)
    if username:
      self.__process_one(username)
    
    self.__process_all()

  
  def __process_all(self):
    retries = 0
    while retries < MAX_RETRIES:
      username = UserFollowsQueue.deque()

      if username is None:
        retries += 1
        time.sleep(CHECK_INTERVAL)
      else:
        retries = 0
        self.__process_one(username)


  def __process_one(self, username):
    global results
    UserFollowsCache.set_currently_processed(username, cid=self.cid)

    if UserFollowsCache.is_processed(username):
      return

    done = False
    while not done:
      try:
        c = twint.Config()
        c.Store_csv = True
        c.User_full = False
        c.Output = "placeholder.csv"
        c.Hide_output = True
        c.Username = username
        twint.run.Following(c)
        done = True
        UserFollowsCache.set_processed(username)
      except:
        results.clear()
        time.sleep(CHECK_INTERVAL)

    with open('../data/collector/follows%s.dat' % self.cid, 'a+', 1) as f:
      f.write("%s %s\n" % (username, json.dumps(results)))

    if results:
      # Follow.update_user_follows(username, results.copy())
      UserDataQueue.enque(results)
    
    results.clear()

# hacky
sys.modules["twint.storage.write"].Csv = __handle_twint_csv
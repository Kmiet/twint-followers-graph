import sys
import time
sys.path.append("..")
import twint
import json
from cache import UserTweetsCache
from queues import UserTweetsQueue

CHECK_INTERVAL=2
MAX_RETRIES=100

results = []

def __handle_twint_json(obj, config):
  global results
  m = obj.__dict__['mentions']
  results.extend(m)


class TweetCollector:

  def __init__(self, collector_id=0):
    self.cid = collector_id
    # self.c = twint.Config()
    # self.c.Store_json = True
    # self.c.User_full = True
    # self.c.Output = "placeholder.json"
    # self.c.Hide_output = True


  def run(self):
    username = UserTweetsCache.get_currently_processed(cid=self.cid)
    if username:
      self.__process_one(username)
    
    self.__process_all()

  
  def __process_all(self):
    retries = 0

    while retries < MAX_RETRIES:
      username = UserTweetsQueue.deque()

      if username is None:
        retries += 1
        time.sleep(CHECK_INTERVAL)
      else:
        retries = 0
        self.__process_one(username)


  def __process_one(self, username):
    global results
    UserTweetsCache.set_currently_processed(username, cid=self.cid)

    if UserTweetsCache.is_processed(username):
      return

    done = False
    while not done:
      try:
        c = twint.Config()
        c.Store_json = True
        c.Custom["tweet"] = ["mentions"] 
        c.Output = "placeholder.json"
        c.Hide_output = True
        c.Username = username
        c.Limit = 200
        twint.run.Search(c)
        done = True
      except:
        time.sleep(2)

    with open('../data/collector/mentions%s.dat' % self.cid, 'a+', 1) as f:
      f.write("%s\n" % json.dumps({ 'username': username , 'mentions': list(results) }) )

    results.clear()

    UserTweetsCache.set_processed(username)

# hacky
sys.modules["twint.storage.write"].Json = __handle_twint_json
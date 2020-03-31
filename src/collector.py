import os
import signal
import argparse
from multiprocessing import Process
from collectors import UserCollector, FollowCollector, TweetCollector

global uprocesses
global fprocesses
global tprocesses

def collect(Collector, cid):
  Collector(collector_id=cid).run()


def signal_handler(sig, frame):
  [child.terminate() for child in uprocesses]
  [child.terminate() for child in fprocesses]
  [child.terminate() for child in tprocesses]


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('uc', type=int)
  parser.add_argument('fc', type=int)
  parser.add_argument('tc', type=int)
  args = parser.parse_args()

  uprocesses = [Process(target=collect, args=(UserCollector, i, )) for i in range(args.uc)]
  fprocesses = [Process(target=collect, args=(FollowCollector, i, )) for i in range(args.fc)]
  tprocesses = [Process(target=collect, args=(TweetCollector, i, )) for i in range(args.tc)]

  [child.start() for child in uprocesses]
  [child.start() for child in fprocesses]
  [child.start() for child in tprocesses]

  signal.signal(signal.SIGINT, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)

  [child.join() for child in uprocesses]
  [child.join() for child in fprocesses]
  [child.join() for child in tprocesses]
  
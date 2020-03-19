import os
import signal
import argparse
from multiprocessing import Process
from collectors import UserCollector, FollowCollector

global uprocesses
global fprocesses

def collect(Collector, cid):
  Collector(collector_id=cid).run()


def signal_handler(sig, frame):
  [child.terminate() for child in uprocesses]
  [child.terminate() for child in fprocesses]


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('uc', type=int)
  parser.add_argument('fc', type=int)
  args = parser.parse_args()

  uprocesses = [Process(target=collect, args=(UserCollector, i, )) for i in range(args.uc)]
  fprocesses = [Process(target=collect, args=(FollowCollector, i, )) for i in range(args.fc)]

  [child.start() for child in uprocesses]
  [child.start() for child in fprocesses]

  signal.signal(signal.SIGINT, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)

  [child.join() for child in uprocesses]
  [child.join() for child in fprocesses]
  
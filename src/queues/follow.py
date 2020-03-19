from .generic import Queue

class FollowQueue(Queue):
  
  def __init__(self):
    super().__init__(suffix='follow:')


UserFollowsQueue = FollowQueue()
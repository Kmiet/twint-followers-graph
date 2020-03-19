from .generic import Queue

class UserQueue(Queue):
  
  def __init__(self):
    super().__init__(suffix='user:')


  def enque(self, msgs):
    super().enque(*msgs)


UserDataQueue = UserQueue()
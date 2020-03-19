from .neo4j_client import getNeo4jClient

class UserRepo:

  def __init__(self):
    self.db = getNeo4jClient()

  
  def update(self, data):
    with self.db.session() as session:
      session.write_transaction(self.__create_or_update, data)

  
  def __create_or_update(self, tx, data):
    tx.run("MERGE (u: User {username: $username}) "
           "SET u.id= $id, u.name = $name, u.bio = $bio, u.location = $location, "
           "u.join_date = $join_date, u.tweets = $tweets, u.follows = $following, "
           "u.followers = $followers, u.likes = $likes, u.media_count = $media_count",
           username=data['username'],
           id=data['id'],
           name=data['name'],
           bio=data['bio'],
           location=data['location'],
           join_date=data['join_date'],
           tweets=data['tweets'],
           following=data['following'],
           followers=data['followers'],
           likes=data['likes'],
           media_count=data['media_count'])

User = UserRepo()
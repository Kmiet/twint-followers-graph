from .neo4j_client import getNeo4jClient

MAX_PER_TRANSACTION=100

class FollowRepo:

  def __init__(self):
    self.db = getNeo4jClient()

  
  def update_user_follows(self, username, followed_users):
    while followed_users:
      batch = followed_users[:MAX_PER_TRANSACTION]
      with self.db.session() as session:
        session.write_transaction(self.__create_or_update, username, batch)
      del followed_users[:MAX_PER_TRANSACTION]

  
  def __create_or_update(self, tx, username, followed_users):
    query = ["MERGE (u: User {username: $username})"]
    for i in range(len(followed_users)):
      query.append(self.__follow_relationship(followed_users[i], i))

    tx.run(" ".join(query), username=username)

  
  def __follow_relationship(self, followed_user, i):
    return ("MERGE (u%d: User {username: '%s'})\n MERGE (u)-[:FOLLOWS]->(u%d)" % (i, followed_user, i))


Follow = FollowRepo()
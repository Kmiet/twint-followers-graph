from neo4j import GraphDatabase

class Neo4jClient:
  __insatnce__ = None
  
  def __init__(self):
    # self.driver = GraphDatabase.driver('bolt://127.0.0.1', encrypted=False)
    self.driver = None


def getNeo4jClient():
  if Neo4jClient.__insatnce__ is None:
    Neo4jClient.__insatnce__ = Neo4jClient()

  return Neo4jClient.__insatnce__.driver 

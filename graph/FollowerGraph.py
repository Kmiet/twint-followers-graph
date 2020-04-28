import networkx as nx

class FollowerGraph:

    def __init__(self):
        self._graph = nx.Graph()


    def add_user(self, username, user_object):
        self._graph.add_node(username)


    def add_follow(self, follower, followed):
        self._graph.add_edge(follower, followed)
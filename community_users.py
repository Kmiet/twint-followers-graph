import networkx as nx
import json

comm_users = dict()

FNAME = 'full_mention_comm'

if __name__ == '__main__':
    G = nx.read_gexf('./%s.gexf' % FNAME)
    user_comm = nx.get_node_attributes(G, 'community')

    for u, c in user_comm.items():
        if not comm_users.get(c):
            comm_users[c] = []

        comm_users[c].append(u)

    with open('./user_comm/%s.txt' % FNAME, 'w+') as f:
        for k, v in comm_users.items():
            f.write('%s %s\n' % (k, json.dumps(v)))


import json
import networkx as nx

FNAME = 'full_mention_comm'
MN = '_mention_comm'
FO = '_follow_comm'

def disrtibution():
    with open('./stats/distribution/%s.txt' % FNAME, 'w+') as f_:
        percentages = {}
        all_count = 0
        with open('./user_comm/%s.txt' % FNAME, 'r') as f:
            line = f.readline()
            while line:
                _comm, _usrs = line.split(' ', 1)
                comm = int(_comm)
                users = json.loads(_usrs)                
                percentages[comm] = len(users)
                all_count += len(users)

                line = f.readline()

            for k in percentages.keys():
                percentages[k] = "%.6f" % (percentages[k] / all_count)

            f_.write(json.dumps(percentages))


def density(G):
    with open('./stats/density/%s.txt' % FNAME, 'w+') as f_:
        comm_users = {}
        densities = {}
        with open('./user_comm/%s.txt' % FNAME, 'r') as f:
            line = f.readline()
            while line:
                _comm, _usrs = line.split(' ', 1)
                comm = int(_comm)
                users = json.loads(_usrs)
                comm_users[comm] = [x for x in users]

                line = f.readline()

        for k in comm_users.keys():
            S = G.subgraph(comm_users[k])
            density = nx.density(S)
            densities[k] = "%.7f" % density
        
        f_.write(json.dumps(densities))


def clustering_coef(G):
    with open('./stats/clustering_coef/%s.txt' % FNAME, 'w+') as f_:
        coef = nx.algorithms.cluster.average_clustering(G)
        f_.write("Avg. of all: %s\n" % str(coef))
        coef = nx.algorithms.cluster.average_clustering(G, count_zeros=False)
        f_.write("Avg. of nonzero coefs: %s\n" % str(coef))


if __name__ == '__main__':
    disrtibution()
    G = nx.read_gexf('./%s.gexf' % FNAME)
    density(G)
    clustering_coef(G)
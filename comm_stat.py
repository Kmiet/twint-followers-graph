import json
import networkx as nx

SMALLER_100 = 'smaller100k'
FULL = 'full'
MN = '_mention_comm'
FO = '_follow_comm'

FNAME = FULL + MN

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


def avg_clustering_coef(G):
    with open('./stats/avg_clustering_coef/%s.txt' % FNAME, 'w+') as f_:
        coef = nx.algorithms.cluster.average_clustering(G)
        f_.write("Avg. of all: %s\n" % str(coef))
        coef = nx.algorithms.cluster.average_clustering(G, count_zeros=False)
        f_.write("Avg. of nonzero coefs: %s\n" % str(coef))


def clustering_coef(G):
    coefs = nx.algorithms.cluster.clustering(G)
    coefs_dist = {}
    for v in coefs.values():
        if not coefs_dist.get(v):
            coefs_dist[v] = 0
        coefs_dist[v] += 1
    with open('./stats/clustering_coef/%s.txt' % FNAME, 'w+') as f_:
        f_.write(json.dumps(coefs_dist))


def degrees(G):
    degree_histogram = nx.degree_histogram(G)
    data = {}
    for i, v in enumerate(degree_histogram):
        data[i] = v

    with open('./stats/node_degrees/%s.txt' % FNAME, 'w+') as f_:
        f_.write(json.dumps(data))


def nodes_n_edges(G):
    with open('./stats/nodes/%s.txt' % FNAME, 'w+') as f_:
        f_.write(str(nx.number_of_nodes(G)))
    
    with open('./stats/edges/%s.txt' % FNAME, 'w+') as f_:
        f_.write(str(nx.number_of_edges(G)))


if __name__ == '__main__':
    # disrtibution()
    G = nx.read_gexf('./%s.gexf' % FNAME)
    # density(G)
    # avg_clustering_coef(G)
    clustering_coef(G)
    degrees(G)
    nodes_n_edges(G)
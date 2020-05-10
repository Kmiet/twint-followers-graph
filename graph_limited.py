import networkx as nx
from os import listdir
from os.path import isfile, join
import json
import random
from graph import FollowerGraph
import time
from infomap import Infomap

DATA_PATH = '../data/collector'
HOW_MANY = 100000

x_users = set()
x_follows = dict()
x_mentions = dict()


def process_user_file(fpath):
    with open(fpath, 'r', 1) as f:
        line = f.readline()
        while line:
            u = json.loads(line)
            x_users.add(u['username'])
            x_follows[u['username']] = []
            
            line = f.readline()
        
        print(fpath, ' file processed.')


def process_follow_file(fpath):
    with open(fpath, 'r', 1) as f:
        line = f.readline()
        i = 0
        while line:
            uname, fls = line.split(' ', 1)
            follows = json.loads(fls)
            if uname in x_users:
                for flw in follows:
                    if flw in x_users:
                        x_follows[uname].append(flw)
            line = f.readline()

        print(fpath, ' file processed.')


def process_mention_file(fpath, G):
    with open(fpath, 'r', 1) as f:
        line = f.readline()
        while line:
            u, smth = line.split('@')[1].split('"')
            ms = smth.split('[')[1].split(']')[0].split(',')
            if u in G.nodes:
                x_mentions[u] = []
                for m in ms:
                    if u != m:
                        x_mentions[u].append(m)

            line = f.readline()


def read_mentions(dirpath, G):
    onlyfiles = [(f, join(dirpath, f)) for f in listdir(dirpath) if isfile(join(dirpath, f))]
    for _rec in onlyfiles:
        fname, fpath = _rec

        if fname.startswith('mentions'):
            process_mention_file(fpath, G)


def create_graph(dirpath):
    G = nx.Graph()
    onlyfiles = [(f, join(dirpath, f)) for f in listdir(dirpath) if isfile(join(dirpath, f))]

    for _rec in onlyfiles:
        fname, fpath = _rec

        if fname.startswith('users'):
            process_user_file(fpath)

    for _rec in onlyfiles:
        fname, fpath = _rec

        if fname.startswith('follows'):
            process_follow_file(fpath)

    u_left = HOW_MANY

    graph_users = []
    que = []
    u_processed = set()
    uname = random.sample(x_users, 1)[0]
    que.append(uname)
    u_processed.add(uname)
    u_left -= 1

    while que:
        u_top = que.pop()
        G.add_node(u_top)
        graph_users.append(u_top)

        for followed in x_follows[u_top]:
            if not followed in u_processed and u_left > 0:
                que.append(followed)
                u_processed.add(followed)
                u_left -= 1

        if u_left > 0 and len(que) == 0:
            while u_top in u_processed:
                u_top = random.sample(x_users, 1)[0]
            que.append(u_top)
            u_processed.add(u_top)
            u_left -= 1

    for node in u_processed:
        for followed in x_follows[node]:
            if followed in u_processed:
                G.add_edge(node, followed)

    return G


def findCommunitiesInfomap(G, v_mentions=False):
    im = Infomap("--two-level --flow-model undirected")

    if v_mentions:
        read_mentions(DATA_PATH, G)

    user_node = dict()
    node_user = []

    l = 0

    for i, n in enumerate(G.nodes):
        l = i
        user_node[n] = l
        node_user.append(n)

    last_l = l

    if not v_mentions:
        for e in G.edges:
            im.addLink(user_node[e[0]], user_node[e[1]])

    else:
        for k, v in x_mentions.items():
            for m in v:
                if not user_node.get(m):
                    user_node[m] = l + 1
                    node_user.append(m)
                im.addLink(user_node[k], user_node[m])

    im.run()

    print("Found %d top modules with codelength: %f" % (im.numTopModules(), im.codelength))

    communities = {}
    for node_id, module_id in im.modules:
        if not node_id > last_l:
            communities[node_user[node_id]] = module_id

    nx.set_node_attributes(G, communities, 'community')
    return im.numTopModules()


if __name__ == '__main__':
    s = time.time()
    # G = create_graph(DATA_PATH)
    # nx.write_gexf(G, "smaller100k.gexf")
    G = nx.read_gexf('./smaller2k.gexf')
    print(G.number_of_nodes(), G.number_of_edges())
    numCommunities = findCommunitiesInfomap(G, v_mentions=False)
    print("Number of communities found: %d" % numCommunities)
    nx.write_gexf(G, "smaller2k_follow_comm.gexf")
    print(time.time()-s)

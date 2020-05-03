import networkx as nx
from os import listdir
from os.path import isfile, join
import json
# import matplotlib.pyplot as plt
import gc
from graph import FollowerGraph
import time
from infomap import Infomap
from networkx.algorithms import community
import matplotlib.pyplot as plt
import numpy as np
import random

# DATA_PATH = '../data/collector'
DATA_PATH = './data/collector'
MENTION_LIMIT = 50

x_users = set()
#
x_mentions = dict()

def process_user_file(fpath, graph):
    with open(fpath, 'r', 1) as f:
        line = f.readline()
        while line:
            u = json.loads(line)
            x_users.add(u['username'])
            graph.add_node(u['username'])
            
            line = f.readline()
        
        print(fpath, ' file processed.')
        f.close()


def process_follow_file(fpath, graph):
    with open(fpath, 'r', 1) as f:
        line = f.readline()
        i = 0
        while line:
            uname, fls = line.split(' ', 1)
            follows = json.loads(fls)
            for flw in follows:
                if flw in x_users:
                    graph.add_edge(uname, flw)
            line = f.readline()
          

        gc.collect()

        print(fpath, ' file processed.')
        f.close()


def process_mention_file(fpath, G):
    with open(fpath, 'r', 1) as f:
        line = f.readline()
        while line:
            u, smth = line.split('@')[1].split('"')
            ms = smth.split('[')[1]
            if not ms.startswith(']'):
                ms = ms.split(']')[0].split(',')
            else:
                ms = []

            if u in G.nodes:
                x_mentions[u] = []
                _curr = 0
                for m in ms:
                    if u != m and _curr < MENTION_LIMIT:
                        x_mentions[u].append(m)
                        _curr += 1

            line = f.readline()


def read_mentions(dirpath, G):
    onlyfiles = [(f, join(dirpath, f)) for f in listdir(dirpath) if isfile(join(dirpath, f))]
    for _rec in onlyfiles:
        fname, fpath = _rec

        if fname.startswith('mentions'):
            process_mention_file(fpath, G)
            print(fpath, ' file processed.')
            gc.collect()


def create_graph(dirpath):
    G = nx.Graph()
    
    onlyfiles = [(f, join(dirpath, f)) for f in listdir(dirpath) if isfile(join(dirpath, f))]

    for _rec in onlyfiles:
        fname, fpath = _rec

        if fname.startswith('users'):
            process_user_file(fpath, G)
            

        gc.collect()

    for _rec in onlyfiles:
        fname, fpath = _rec

        if fname.startswith('follows'):
            process_follow_file(fpath, G)

        gc.collect()

    return G


def findCommunitiesInfomap(G, v_mentions=False):
    im = Infomap("--two-level --flow-model directed")

    if v_mentions:
        read_mentions(DATA_PATH, G)
    
    return 0

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

def label_propagation_algorithm(G):
    return community.asyn_lpa_communities(G)

def get_cmap(n, name='hsv'):
    return plt.cm.get_cmap(name, n)

color = lambda : [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

if __name__ == '__main__':
    s = time.time()
    # G = create_graph(DATA_PATH)
    # nx.write_gexf(G, "full.gexf")
    G = nx.read_gexf('./smaller100k.gexf')
    print(G.number_of_nodes(), G.number_of_edges())
    # numCommunities = findCommunitiesInfomap(G, v_mentions=True)
    # print("Number of communities found: %d" % numCommunities)
    communities_generator = label_propagation_algorithm(G)
    top_level_communities = next(communities_generator)
    next_level_communities = next(communities_generator)
    # print(sorted(map(sorted, next_level_communities)))

    result = {frozenset(c) for c in communities_generator}

    nodes_community = list(result)
    print(len(nodes_community))

    # pos = nx.spring_layout(G) 

    # nx.draw(G, pos, edge_color='k',  with_labels=True,
    #         font_weight='light', node_size= 280, width= 0.9)
    
    cmap = get_cmap(len(nodes_community))

    for i in nodes_community:
        c = tuple(np.random.randint(256, size=3)) + (0,)
        # nx.draw_networkx_nodes(G, pos, nodelist=i, node_color=cmap(nodes_community.index(i)))
        for node in i:
            # print(node)
            G.nodes[node]['viz'] = {'color': {'r': c[0], 'g': c[1], 'b': c[2], 'a': c[3]}}

    nx.write_gexf(G, 'example100k.gexf')

    # plt.savefig('graphe100k.png')
    # plt.show()

    print(time.time()-s)

import networkx as nx
from os import listdir
from os.path import isfile, join
import json
import matplotlib.pyplot as plt
import gc
from graph import FollowerGraph
import time

x_users = set()

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


# def process_mention_file(fpath):
#     with open(fpath, 'r', 1) as f:
#         line = f.readline()
#         while line:
#             line = f.readline()


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


if __name__ == '__main__':
    s = time.time()
    G = create_graph('./data/collector')
    nx.write_gexf(G, "test.gexf")
    print(time.time()-s)

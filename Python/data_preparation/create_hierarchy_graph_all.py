"""
To create a file out of the geographical hierarchies, using the hierarchical triples.
This is the generalized version of Hierarchies_Graph.py, which does the same for all PROVs all together.
All PROVs are integrated in a single graph. The graph also will be traversed to find the hierarchies from PROV to STTL.
Then, the hierarchies resulting from the traversal will be written a file in which each line starts with the most top level division and ends with sttls.
Also, creates a json to be used in visualizations.
"""
import io
import json
import os

import networkx as nx
from networkx.readwrite import json_graph

from aratext import normalization as norm


# reload(sys)
# sys.setdefaultencoding('utf8')

def get_set_of_name(file_name, name):
    roots = set()
    with open(file_name, "r") as f1:
        f1 = f1.read().split("\n")
        for l in f1:
            lS = l.split("\t")
            if lS[0].startswith(name):
                roots.add(lS[0])
    return roots


cnt = 2
count = 0


def graph_level(g, file_name, node_id, trav):
    """
  To traverse the graph and form individual routes from PROV to STTL, expressing single hierarchies.
  """
    global cnt
    global count

    with open(file_name, "r") as f1:
        f1 = f1.read().split("\n")
        found = False

        for l in f1:
            lS = l.split("\t")
            if lS[0] == g.node[node_id]['label'] or \
                    norm.normalize_alphabet(lS[0]) == norm.normalize_alphabet(g.node[node_id]['label']):
                found = True
                ident = cnt
                g.add_node(ident, label=lS[-1])
                g.add_edge(node_id, ident, label=lS[1])
                cnt = cnt + 1
                if 'STTL' not in g.node[ident]['label']:
                    trav.append(lS[1])
                    trav.append('' + g.node[ident]['label'])
                    graph_level(g, file_name, ident, trav)
                    trav.pop()
                    trav.pop()
                else:
                    found = True
                    count = count + 1
                    trav.append(lS[1])
                    trav.append('' + g.node[ident]['label'])
                    a = ''
                    # with open("../Data/" + fileName+"_H3", "a") as f2:
                    with open("/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_hier_all", "a") as f2:
                        f2.write(','.join(trav))
                        f2.write('\n')
                    trav.pop()
                    trav.pop()
        if found == False:
            # print(trav)
            # with open("../Data/Muqaddasi/" + fileName+"_H4", "a") as f2:
            with open("/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_hier_all", "a") as f2:
                f2.write(','.join(trav))
                f2.write('\n')


def build_hier_graph(file_name, write_file):
    """
    Main functoin to build the graph and write it to a file.
    It also creats a json representation of the hierarchies.
    """
    global cnt
    data = []
    print(file_name)
    roots = get_set_of_name(file_name, "PROV")
    graphs = []
    g = nx.DiGraph()
    g.add_node(1, label="root")
    # remove the content of destination file to write new content.
    # later we will append to this file
    with open(write_file, "w"):
        pass
    for rs in roots:
        trav = []
        g.add_edge(1, cnt, label="child of root")
        g.add_node(cnt, label=rs)
        trav.append('' + g.node[cnt]['label'])
        # trav.append(lS[1])
        cnt = cnt + 1
        graph_level(g, file_name, cnt - 1, trav)

    data = json_graph.tree_data(g, root=1)
    nx.write_edgelist(g, "muq_edgelist", delimiter="\t")
    with io.open('/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/tree' + g.node[1]['label'] + '.json',
                 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))


# buildHierarchiesGraph("../Data/Shamela_0023696_Triples_H4")
build_hier_graph("/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_triples_hier",
                 "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_hier_all")
print(count)

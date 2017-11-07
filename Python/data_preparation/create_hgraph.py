import networkx as nx
# import matplotlib.pyplot as plt

def create_hgraph(file_name):
    with open(file_name, "r") as f1:
        f1 = f1.read().split("\n")
        g = nx.Graph()
        for line in f1:
            vs = line.split("\t")
            g.add_edge(vs[0],vs[0] + " - " + vs[-1])
        nx.write_edgelist(g, "test.edgelist", delimiter="\t")

    # data = json_graph.tree_data(g,root=1)
    # with io.open('/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/tree2'+g.node[1]['label']+'.json', 'w', encoding='utf-8') as f:
    #   f.write(json.dumps(data, ensure_ascii=False))
    # nx.draw(g, pos=nx.spring_layout(g))
    # plt.show()
create_hgraph("/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_triples_hier")
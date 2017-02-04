from networkx.readwrite import json_graph
import io, json
import re
import networkx as nx
import matplotlib.pyplot as plt	
import sys  
from decimal import *
from pyproj import *
import global_var as gv
import numpy as np
import matplotlib.pyplot as plt


def dfs_on_geoNet(geoNetFile):
    with open(geoNetFile) as cgraphfile:    
      data = json.load(cgraphfile)
      G = json_graph.node_link_graph(data)
      bfs = []
      for node in gv.metropoles:
        if node in G.nodes():
          print(node, "\n")
          t = nx.bfs_tree(G, node)
          #print(t.nodes())
          pos = nx.spring_layout(t)
          labels = nx.draw_networkx_labels(t,pos)
          #print(labels)
          nx.draw_networkx_nodes(t, pos, cmap=plt.get_cmap('jet'),with_labels=True)
          nx.draw_networkx_edges(G, pos, edgelist=t.edges(), edge_color='r')
          #labels = nx.draw_networkx_labels(g,pos)
          print("nodes: ",len(t.nodes()))
          print("edges: ",len(t.edges()))
          plt.axis('off')
          plt.savefig("../Data/pics/muq_dfs_metropoles/dfs_" + node + ".png", bbox_inches=0, pad_inches=0.1)#orientation='landscape',) 
          plt.show()


dfs_on_geoNet("Muqaddasi_Graph.json")
print("done!")

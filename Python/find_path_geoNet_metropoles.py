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


def read_graph(geoNetFile):
  with open(geoNetFile) as cgraphfile:    
      data = json.load(cgraphfile)
      G = json_graph.node_link_graph(data)
      return G

# Find shortest paths between metropoles
def metropoles_shortest_paths(geoNetFile):
      G = read_graph(geoNetFile)
      for i in range(len(gv.metropoles)):
          for j in range(i+1, len(gv.metropoles)):
            if gv.metropoles[i] in G.nodes() and gv.metropoles[j] in G.nodes():
              print(gv.metropoles[i], " - ", gv.metropoles[j], "\n")
              try:
                print([p for p in nx.all_shortest_paths(G, gv.metropoles[i], gv.metropoles[j])])
                #print(n)
              except nx.NetworkXNoPath:
                print('No path')
        
# Find shortest paths between all nodes.
def all_shortest_paths(geoNetFile):
      G = read_graph(geoNetFile)
      paths = dict()
      for node in G.nodes():
        #print(node, "\n")
        try:
          paths.update(nx.all_pairs_shortest_path(G))
                #print(n)
        except nx.NetworkXNoPath:
          print('No path')
      print("paths: ", paths)
      with open('Muqaddasi_all_shortest_paths.json', 'w') as graphfile:
          json.dump(paths, graphfile, ensure_ascii=False, indent=4)

all_shortest_paths("Muqaddasi_Graph_noNorm_noAL_origkey90.json")
print("done!")

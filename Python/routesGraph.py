# To create a file out of the geographical routes, using the route triples.
# Each line in the file starts with the source(from), then destination comes and ends with distance (in meter).
# Also, creates a json to be used in visualizations.

from networkx.readwrite import json_graph
import io, json, csv
import re
import networkx as nx
import matplotlib.pyplot as plt	
import sys  

def createGraph(fileName):
    #roots = set()
    
   G = nx.read_edgelist(fileName, delimiter=",", data=[("Distance_Meter", float)], encoding="utf8")
   G.edges(data=True)
   edge_labels = dict( ((u, v), d["Distance_Meter"]) for u, v, d in G.edges(data=True) )
   pos = nx.random_layout(G)
   #nx.draw(G, pos)
   #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
   #plt.show()
   with open(fileName, "r") as routesFile:
    routesFile =csv.reader(routesFile, delimiter=',', quotechar='|')
    for r in routesFile:
      print(r[0], " ", G[r[0]])
       

	
createGraph("../Data/tripleRoutes_withMeter")


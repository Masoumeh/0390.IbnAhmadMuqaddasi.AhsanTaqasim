from networkx.readwrite import json_graph
import io, json, csv
import re
import networkx as nx
import matplotlib.pyplot as plt	
import sys  
from decimal import *
from pyproj import *
from shapely.geometry import *
from shapely.ops import cascaded_union
#from rtree import index

# Calculated distance and bearing between 2 GPS points
from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km


def createGraph(fileName):
    #roots = set()
    
   #G = nx.read_edgelist(fileName, delimiter=",", data=[("Distance_Meter", float)], encoding="utf8")
   #G.edges(data=True)
   #edge_labels = dict( ((u, v), d["Distance_Meter"]) for u, v, d in G.edges(data=True) )
   G = nx.Graph()
   getcontext().prec = 4
   with open(fileName, 'r') as meterFile:
      distReader = csv.DictReader(meterFile, delimiter=',')
      #next(distReader, None)
      rows = list(distReader)
      for row in rows:
        #print(row['From'], row['From_lat'], row['From_long'])
        #print(row['To'], row['To_lat'], row['To_long'])
        G.add_node(row['From'], lat=row['From_lat'], lng=row['From_long'])
        G.add_node(row['To'], lat=row['To_lat'], lng=row['To_long'])
        G.add_edge(row['From'],row['To'], length= row['Distance_avgMeter'])
   # find nodes without coordinate
   null_coord_nodes = []
   for node in G.nodes():
     if G.node[node]['lat'] == "null" and G.node[node]['lng'] == "null":
       null_coord_nodes.append(node)
       #print("node", node)
   #print(len(null_coord_nodes))
   with open('../Data/bfs.json', 'w') as outfile:
     for node in null_coord_nodes:
        json.dump(nx.bfs_successors(G,node), outfile, ensure_ascii=False, indent=4)

   with open('../Data/neighbours_forNulls', 'w') as f:
     Writer = csv.writer(f, delimiter=',',)
     #fWriter.writerow(["lat", "lng", "name", "property"])
     for node in null_coord_nodes:
       #neighbors[node] = []
       #for n in G.neighbors(node):
         #if G.node[n]['lat'] != "null" and G.node[n]['lng'] != "null": 
       Writer.writerow([node, G.neighbors(node)])
     #print(nx.bfs_successors(G,node))
  
createGraph("../Data/tripleRoutes_withMeter2")


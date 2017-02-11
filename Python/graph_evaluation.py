"""
To get some information from the route network graph, like how far are the first two neighbours (with coords) of a node (without coords)
"""

from networkx.readwrite import json_graph
import io, json, csv
import re
import networkx as nx
import sys  
import operator
import compose_graphs as cg

def findNeighbours_of_Nulls(G, writer):
   #G = nx.Graph()
   #G = cg.composeGraphs(textRoutes, cornuRoutes, cornuPlaces)
   '''with open(fileName, 'r') as meterFile:
      distReader = csv.reader(meterFile, delimiter=',')
      next(distReader, None)
      for row in distReader:
        G.add_node(row[0], lat=row[1], lng=row[2])
        G.add_node(row[3], lat=row[4], lng=row[5])
        G.add_edge(row[0],row[3], length= row[-1])'''
   coord_neighbors = {}     
   nulls = [n for n in G.nodes() if G.node[n]['lat'] == "null" and G.node[n]['lng'] == "null"]
   print(len(nulls))
   for node in nulls:
     length = nx.single_source_shortest_path_length(G,node)
     sorted_length = sorted(length.items(), key=operator.itemgetter(1))
     neighCoords = []
     # exclude the firs item of list from the loop which is the node itself with the distance of zero from the node! i.e. ('node',0)
     for l in sorted_length[1:]:
       # check the distance of node from the neigbor and if the neighbor has coordinate
       if 0 < l[1] and G.node[l[0]]['lat'] != "null" and G.node[l[0]]['lng'] != "null":
           # add the neighbor to array
           neighCoords.append( [l[0],l[1]])
       # limit the neighbors to two to have at leat two neighbours with 
       if len(neighCoords) >= 2:
         break
     writer.writerow([node,neighCoords])
	

with open('../Data/nulls_withCoordNeighbors.csv', 'w', encoding='utf8') as outfile:
  writer = csv.writer(outfile, delimiter=',')
  writer.writerow(["node_without_coord", "nearest_coords"])
  findNeighbours_of_Nulls("../Data/tripleRoutes_withMeter2_normalized2", "../Data/all_routes_new.json", "../Data/places.geojson", writer)
print("done!")


''' Visualize graph based on the node 'status' attribute to see which nodes have coordinates and which do not. '''
from __future__ import unicode_literals
#from bidi import algorithm as bidialg
import createGraphFromCSV as cgCSV
import createGraphFromJSON as cgJS
import compose_graphs as cmpg
import networkx as nx
import matplotlib.pyplot as plt
from itertools import count
import numpy as np
import csv, json

def vis_graph(csvFile, jsonFile, cornuPlaces):
  #G = cg.createGraphFromCSV(fileName)
  G = cmpg.composeGraphs(csvFile, jsonFile, cornuPlaces)
  #with open("../Data/newCoords_composedGraph_bufferCenter_before.csv", "w", encoding="utf8") as firstGraph:
  #   writer1 = csv.writer(firstGraph, delimiter=',')
  #   writer1.writerow(["name", "lat", "lng", "status"])
  # get the list of connected components as subgraphs
  '''graphs = list(nx.connected_component_subgraphs(G))
  # get different values for ststus attribute
  status = set(nx.get_node_attributes(G,'status').values())
  print(status)
  # map each status value to a numeric value; with current data we will have {'old': 1, 'null': 0}
  mapping = dict(zip(sorted(status),count()))
  # here we try visualization only on a subgraph (graphs[1])
  cnt = 0;
  for g in graphs:
    cnt += 1
    nodes = g.nodes()
    # assign colors to each node based on the status values
    colors = [mapping[g.node[n]['status']] for n in nodes]
    #fig, ax = plt.subplots()
    # drawing nodes and edges separately so we can capture collection for colobar
    pos = nx.spring_layout(g) # positions of nodes
    #fig, ax = plt.subplots()
    ec = nx.draw_networkx_edges(g, pos, alpha=0.2)
    nc = nx.draw_networkx_nodes(g, pos, nodelist=nodes, node_color=colors, 
                            with_labels=True, node_size=50, cmap=plt.cm.jet)
    labels = nx.draw_networkx_labels(g,pos)
    #plt.colorbar(nc)
    plt.axis('off')
    #xy = np.row_stack([point for key, point in pos.items()])
    #x, y = np.median(xy, axis=0)
    #ax.set_xlim(x-0.6, x+0.6)
    #ax.set_ylim(y-0.6, y+0.6)
    # save as png
    plt.savefig("../Data/pics/composedGraph/subgraph_coordStatus_" + str(cnt) + ".png", bbox_inches=0, pad_inches=0.1)#orientation='landscape',) 
    plt.close()'''
    #plt.show()


vis_graph("../Data/tripleRoutes_withMeter2_normalized_with_region", "../Data/routes.json", "../Data/places.geojson")

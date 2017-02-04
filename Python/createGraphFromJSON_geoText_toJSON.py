from networkx.readwrite import json_graph
import io, json
import re
import networkx as nx
import matplotlib.pyplot as plt	
import sys  
from decimal import *
from pyproj import *


def createGraph(geoRoutesFile, cornuPlaces):
   G = nx.Graph()
  # Add from Muqaddasi
   with open(geoRoutesFile, 'r') as grFile:
      distReader = json.load(grFile)
      for r in distReader:
        startURI = distReader[r]['start']['URI']
        startReg = distReader[r]['start']['region']
        startNode = startURI + "," + startReg if startURI != "null" else r.split("+")[0] 
        endURI = distReader[r]['end']['URI']
        endReg = distReader[r]['end']['region']
        endNode = endURI + "," + endReg if endURI != "null" else r.split("+")[1]
        print(startNode)
        G.add_node(startNode, lat= distReader[r]['start']['lat'], lng= distReader[r]['start']['lon'], status="old" if distReader[r]['start']['URI'] != "null" else "null", region=distReader[r]['start']['region'])
        print(endNode)
        G.add_node(endNode, lat= distReader[r]['end']['lat'], lng= distReader[r]['end']['lon'], status="old" if distReader[r]['end']['URI'] != "null" else "null", region=distReader[r]['end']['region'])
        G.add_edge(startNode, endNode, length= distReader[r]['cornu_meter'])
   data = json_graph.node_link_data(G)
   with open('Muqaddasi_Graph_noNorm_noAL.json', 'w') as graphfile:
          json.dump(data, graphfile, ensure_ascii=False, indent=4) 

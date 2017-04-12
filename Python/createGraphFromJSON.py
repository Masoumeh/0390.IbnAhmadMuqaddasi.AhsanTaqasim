from networkx.readwrite import json_graph
import io, json, csv
import re
import networkx as nx
import matplotlib.pyplot as plt	
import sys  
import math
from decimal import *
from pyproj import *


def createGraphFromJSON(fileName):
   G = nx.Graph()
   with open(fileName) as jsonFile:    
      allData = json.load(jsonFile)
      for d in allData['features']:
        G.add_node(d['properties']['sToponym'], lat="TBA", lng="TBA", status="old")
        G.add_node(d['properties']['eToponym'], lat="TBA", lng="TBA", status="old")
        G.add_edge(d['properties']['sToponym'] ,d['properties']['eToponym'], length= d['properties']['Meter'])
   return G

from networkx.readwrite import json_graph
import io, json, csv
import re
import networkx as nx
import matplotlib.pyplot as plt	
import sys  
import math
from decimal import *
from pyproj import *


def createGraphFromCSV(fileName):
   G = nx.Graph()
#   getcontext().prec = 4
   #proj1 = Proj(init='epsg:26915')
   #project = partial(
   # transform,
   # Proj(init='epsg:4326'), # source coordinate system
   # Proj(init='epsg:26915')) # destination coordinate system
   with open(fileName, 'r') as meterFile:
      distReader = csv.reader(meterFile, delimiter=',')
      next(distReader, None)
      for row in distReader:
        G.add_node(row[4] if row[4] != "null" else row[0], lat=row[1], lng=row[2], status="old" if row[1] != "null" and row[2] != "null" else "null")
        G.add_node(row[9] if row[9] != "null" else row[5], lat=row[6], lng=row[7], status="old" if row[6] != "null" and row[7] != "null" else "null")
        G.add_edge(row[4] if row[4] != "null" else row[0] ,row[9] if row[9] != "null" else row[5], length= row[-1])
   return G

import networkx as nx
import aratext.normalization as norm
import pandas as pan
import json
from itertools import *


def create_graph_csv(file_name):
   G = nx.Graph()
   with open(file_name, 'r', encoding="utf8") as routes_file:
      # dist_reader = csv.reader(meterFile, delimiter='\t')
      # For Muq data
      # dist_reader = pan.read_csv(routes_file, delimiter='\t', names=["from", "from_reg", "to", "to_reg", "distance"])
      # For chiara data
      dist_reader = pan.read_csv(routes_file, delimiter='\t', names=["from", "to", "distance"])
      # cnt  = 0
      for index,row in islice(dist_reader.iterrows(), 1, None):
        # cnt += 1
        # print(row['from'], " ", row['to'])
        # for Muq data
        # s = norm.normalize_alphabet(row["from"].strip()) + "/" + row["from_reg"]
        # e = norm.normalize_alphabet(row["to"].strip()) + "/" + row["to_reg"]
        # for chiara's data
        s = (row["from"].strip()).title()
        e = (row["to"].strip()).title()
        # for both
        G.add_node(s, cano_name=[], coord=[], matches=[])
        G.add_node(e, cano_name=[], coord=[], matches=[])
        # for Chiara
        # G.add_edge(s, e)
                   #length=row["distance"])
        # for Muq
        G.add_edge(s, e, length=row["distance"])

   # pos = nx.graphviz_layout(G)
   return G

def create_graph_geojson(file_name, places_file):
   G = nx.Graph()
   s_found = False
   e_found = False
   with open(file_name, 'r', encoding="utf8") as routes_file:
      dist_reader = json.load(routes_file)
      with open(places_file, 'r', encoding="utf8") as places:
          place_reader = json.load(places)
          for r in dist_reader['features']:
              s_uri = r['properties']['sToponym']
              e_uri = r['properties']['eToponym']
              for p in place_reader['features']:
                 uri = p['properties']['althurayyaData']['URI']
                 if uri == s_uri:
                     s_found = True
                     G.add_node(s_uri, ar_name= p['properties']['althurayyaData']['names']['ara']['common'],
                                ar_name_other= p['properties']['althurayyaData']['names']['ara']['common_other'])
                 if uri == e_uri:
                     e_found = True
                     G.add_node(e_uri, ar_name= p['properties']['althurayyaData']['names']['ara']['common'],
                                ar_name_other= p['properties']['althurayyaData']['names']['ara']['common_other'])
                 if s_found == True and e_found == True:
                     G.add_edge(s_uri, e_uri, length=r['properties']['Meter'], id=r['properties']['id'])
   # # pos = nx.graphviz_layout(G)
   return G
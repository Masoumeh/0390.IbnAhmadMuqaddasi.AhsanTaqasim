import createGraphFromJSON as cg
import networkx as nx
import json, csv
from net_simplification import graph


# cornu_net = open("../Data/routes.json", 'r')
# try:
#     import pygraphviz
#     from networkx.drawing.nx_agraph import write_dot
#     print("using package pygraphviz")
# except ImportError:
#     try:
#         import pydotplus
#         from networkx.drawing.nx_pydot import write_dot
#         print("using package pydotplus")
#     except ImportError:
#         print()
#         print("Both pygraphviz and pydotplus were not found ")
#         print("see http://networkx.github.io/documentation"
#               "/latest/reference/drawing.html for info")
#         print()
#         raise
# graph = cg.createGraphFromJSON("../Data/routes.json")
nodes = dict()
f2 = open("../Data/places.geojson", 'r')
json_uris = json.load(f2)
with open("../Data/routes.json") as jsonFile:
      allData = json.load(jsonFile)
      for d in allData['features']:
          coord = graph.find_coords_of_uri(d['properties']['sToponym'], json_uris)
          nodes[d['properties']['sToponym']] = {"lat":coord[0][0], "lon": coord[0][1]}
          coord = graph.find_coords_of_uri(d['properties']['eToponym'], json_uris)
          nodes[d['properties']['eToponym']] = {"lat":coord[0][0], "lon": coord[0][1]}

with open("../Data/cornu_nodes_list.csv", "w") as outFile:
    fieldnames = ['node', 'lat', 'lon']
    writer = csv.DictWriter(outFile, fieldnames=fieldnames)
    writer.writeheader()
    for n in nodes:
        writer.writerow({'node': n, 'lat': nodes[n]['lat'], 'lon': nodes[n]['lon']})



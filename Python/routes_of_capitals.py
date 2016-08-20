# To biuld the routes starting and ending with capitals from geogrpahic text (like Muqaddasi!)

import io, json
import re
import sys, codecs
import csv
import networkx as nx


# makes a list of capitals 
def getcapitals(fileName):
    capitals = list()
    with open(fileName, "r", encoding="utf8") as hierFile:
        hierFile = csv.reader(hierFile, delimiter=',')
        for hier in hierFile:
          if hier[-2][4:].strip() == "قصبة":
            capitals.append(hier[-1][4:].strip())
    print("count: ", len(capitals))
    return capitals

# Creat route graph 
def createGraph(fileName):

   G = nx.read_edgelist(fileName, delimiter=",", data=[("Distance_Meter", float)], encoding="utf8")
   G.edges(data=True)
   edge_labels = dict( ((u, v), d["Distance_Meter"]) for u, v, d in G.edges(data=True) )
   return G

# Find the routes 
def findRoutes(routeFile, hierFile):
    capitals = getcapitals(hierFile)
    print(capitals)
    G = createGraph(routeFile)
    paths = []
      #fWriter.writerow(["geoTitle", "cornuTitle", "cornuTitleOther", "lat", "lon", "cornuRegion", "geoProv", "geoFinalReg", "eiSearch", "translitTitle", "FW_ratio"])
    for capi in capitals:
      tmpArray = capitals[capitals.index(capi)+1:]
      for nxtCapi in tmpArray:
        if capi in G.nodes() and nxtCapi in G.nodes():
          try:
            for path in nx.all_shortest_paths(G,capi, nxtCapi):
            #print n
              paths.append(path)
          except nx.NetworkXNoPath:
            #print ('No path from ', capi, ' to ', nxtCapi)
            paths.append([capi, 'no Path', nxtCapi])
#          for path in nx.all_shortest_paths(G, source=capi, target=nxtCapi):  
      #tmp = nx.all_simple_paths(G, source=capitals[0], target=capitals[1]):
      #print(paths)
            
    with open("../Data/routes_of_capitals", 'w', encoding="utf8") as capiRoutes:
      fWriter = csv.writer(capiRoutes, delimiter=',', quoting=csv.QUOTE_MINIMAL)
      for path in paths:
        fWriter.writerow(path)

findRoutes("../Data/tripleRoutes_withMeter", "../Data/Shamela_0023696_Triples_H")
print("done!")

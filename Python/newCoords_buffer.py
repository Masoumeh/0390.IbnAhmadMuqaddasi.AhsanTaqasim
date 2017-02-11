from networkx.readwrite import json_graph
import io, json, csv
import re
import networkx as nx
import matplotlib.pyplot as plt	
import sys  
import math
from decimal import *
from geopy.distance import vincenty
from pyproj import *
from shapely.geometry import *
from shapely.wkt import *
from functools import partial
import compose_graphs_json as cmpg
import haversine as haver
import findNeighbors_of_Nulls as fNN

def createGraph(textRoutes, cornuRoutes, cornuPlaces):
   G = nx.Graph()
   getcontext().prec = 4
   proj1 = Proj(init='epsg:26915')
   project = partial(
    transform,
    Proj(init='epsg:4326'), # source coordinate system
    Proj(init='epsg:26915')) # destination coordinate system
   #G = cmpg.composeGraphs(textRoutes, cornuRoutes, cornuPlaces)
   #return
   with open("composedGraph_json2.json") as cgraphfile:    
      data = json.load(cgraphfile)
      G = json_graph.node_link_graph(data)
   neighbors = dict()
   # Write the graph nodes to csv file before finding null coordinates
   #with open("../Data/newCoords_composedGraph_bufferCenter_before2.csv", "w", encoding="utf8") as firstGraph:
   #  writer1 = csv.writer(firstGraph, delimiter=',')
   #  writer1.writerow(["name", "lat", "lng", "status"])
   #  for node in G.nodes():
   #    writer1.writerow([node, G.node[node]['lat'], G.node[node]['lng'], G.node[node]['status']])

   # holding the number of nodes with null coordinate and more than one neighbor
   #with open('../Data/nulls_withCoordNeighborsLen1.csv', 'w', encoding='utf8') as outfile:
   # writer = csv.writer(outfile, delimiter=',')
   # writer.writerow(["node_without_coord", "nearest_coords"])
   # fNN.findNeighbors_of_Nulls(G, writer)
   #return
   found = len([n for n in G.nodes() if G.node[n]['lat'] == "null" and G.node[n]['lng'] == "null" and len(G.neighbors(n)) > 1])
   print(found)
   # check neighbors of nodes without coordinate, whether they have coordinate or not
   with open("../Data/newCoords_composedGraph_bufferCenter_fromJSON.csv", "w", encoding="utf8") as newCoordFile:
     fWriter = csv.writer(newCoordFile, delimiter=',',)
     fWriter.writerow(["geometry", "name", "cenroid", "centerLat", "centerLon"])
     prev_found = 0
     not_intersected = {}
     cnt = 0
     while (found != prev_found ):
       prev_found = found
       print(prev_found ,found)
       print("cnt: ", cnt)
       for node in G.nodes():
         if G.node[node]['lat'] == "null" and G.node[node]['lng'] == "null" and len(G.neighbors(node)) > 1: 
           neighbors[node] = []
           for n in G.neighbors(node):
             if G.node[n]['lat'] != "null" and G.node[n]['lng'] != "null": 
               neighbors[node].append(n) 
           #print("neigh: ",node, "+ ", neighbors[node])
           #return
           # TODO: check nodes with one neighbour 
           # if a point has more than two neighbours in the network 
           neiLen = len(neighbors[node])
           if neiLen >= 2:
             cnt = cnt +1
             x1,y1 = proj1(G.node[neighbors[node][0]]['lat'],G.node[neighbors[node][0]]['lng'])
             x2,y2 = proj1(G.node[neighbors[node][1]]['lat'],G.node[neighbors[node][1]]['lng'])

             # r1 and r2, distances between node and the first two neighbours
             r1 = G[node][neighbors[node][0]]['length']
             r2 = G[node][neighbors[node][1]]['length']
             if r1 != "null" and r2 != "null":

               circle1 = Point(x1, y1).buffer(Decimal(r1)).boundary
               circle2 = Point(x2, y2).buffer(Decimal(r2)).boundary
              #fWriter.writerow(["{0:4f}".format(newX), "{0:4f}".format(newY), "new"])
             #if not circle1.intersects(circle2):
             #  fWriter.writerow(["null","null",node, "new"])
             #for nei in neighbors[node]:
             #print("nei: ",nei)
             #  fWriter.writerow([G.node[nei]['lat'],G.node[nei]['lng'], nei, "old"])
               if circle1.intersects(circle2):
                 newLatProj1,newLonProj1 = circle1.intersection(circle2).geoms[0].coords[0][0],circle1.intersection(circle2).geoms[0].coords[0][1]
                 newLatProj2,newLonProj2 = circle1.intersection(circle2).geoms[1].coords[0][0],circle1.intersection(circle2).geoms[1].coords[0][1]
                # coordintes projected back to in wgs84
                 newLat1, newLon1 = proj1(newLatProj1,newLonProj1, inverse = True)
                 newLat2, newLon2 = proj1(newLatProj2,newLonProj2, inverse = True)
               # line and then the its buffer created out of points in projected system
               #lineP = LineString([Point(newLatProj1,newLonProj1), Point(newLatProj2,newLonProj2)]).buffer(1000)
               # line and then the its buffer created out of points in wgs84
                 geometry = LineString([Point(newLat1,newLon1), Point(newLat2,newLon2)]).buffer(0.001)
                 centerLat = geometry.centroid.coords[0][0]
                 centerLon = geometry.centroid.coords[0][1]
               #coordArr = []
               #for coord in lineP.exterior.coords:
               #  coord = proj1(coord[0],coord[1],inverse=True)
               #  coordArr.append(coord)
               #poly = Polygon(coordArr)
               #print(poly)
#                 tmpX, tmpY = proj1(coord[0], coord[1])
                 fWriter.writerow([ geometry, node, geometry.centroid,  centerLat, centerLon])
               #fWriter.writerow([float("{0:0.5f}".format(newLat2)),float("{0:0.5f}".format(newLon2)),node])
                 G.node[node]['lat'] = centerLat
                 G.node[node]['lng'] = centerLon
                 G.node[node]['status'] = "new"
                 found = found - 1
               else:
                 if node not in not_intersected:
                   not_intersected[node] = {}
                   not_intersected[node]['neighor1'] = neighbors[node][0]
                   not_intersected[node]['neighor2'] = neighbors[node][1]
                   not_intersected[node]['dist1'] = r1
                   not_intersected[node]['dist2'] = r2
                   not_intersected[node]['haversine distance'] = haver.haversine(float(G.node[neighbors[node][0]]['lng']), float(G.node[neighbors[node][0]]['lat']), float(G.node[neighbors[node][1]]['lng']), float(G.node[neighbors[node][1]]['lat']))
   #print(not_intersected)
   with open("../Data/newCoords_composedGraph_bufferCenter_with_region_fromJSON.csv", "w", encoding="utf8") as newGraph:
     #json.dump(featureColl, newGraph, ensure_ascii=False, indent=4)  
     fWriter = csv.writer(newGraph, delimiter=',')
     fWriter.writerow(["name", "lat", "lng", "status"])
     for node in G.nodes():
       fWriter.writerow([node, G.node[node]['lat'], G.node[node]['lng'], G.node[node]['status']])
   with open("../Data/newCoords_composedGraph_notIntersected_with_region_fromJSON.csv", "w", encoding="utf8") as newGraph:
     json.dump(not_intersected, newGraph, ensure_ascii=False, indent=4)  
     
	
createGraph("../Data/tripleRoutes_withMeter2_normalized_with_cornuRegion_json","../Data/routes.json", "../Data/places.geojson")


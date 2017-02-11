"""

"""

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

def createGraph(fileName):
     G = nx.Graph()
     getcontext().prec = 4
     proj1 = Proj(init='epsg:26915')
     project = partial(
       transform,
       Proj(init='epsg:4326'), # source coordinate system
       Proj(init='epsg:26915')) # destination coordinate system
     with open(fileName, 'r') as meterFile:
       distReader = csv.reader(meterFile, delimiter=',')
       next(distReader, None)
       for row in distReader:
         G.add_node(row[0], lat=row[2], lng=row[1], status="old" if row[1] != "null" and row[2] != "null" else "null")
         G.add_node(row[3], lat=row[5], lng=row[4], status="old" if row[4] != "null" and row[4] != "null" else "null")
         G.add_edge(row[0],row[3], length= row[-1])
     neighbors = dict()
   # Write the graph nodes to csv file before finding null coordinates
   #with open("../Data/newCoords_graph_bufferCenter_before.csv", "w", encoding="utf8") as firstGraph:
   #  writer1 = csv.writer(firstGraph, delimiter=',')
   #  writer1.writerow(["name", "lat", "lng", "status"])
   #  for node in G.nodes():
   #    writer1.writerow([node, G.node[node]['lat'], G.node[node]['lng'], G.node[node]['status']])

   # holding the number of nodes with null coordinate and more than one neighbor
     found = len([n for n in G.nodes() if G.node[n]['lat'] == "null" and G.node[n]['lng'] == "null" and len(G.neighbors(n)) > 1])

     featureColl = {}
     featureColl['type'] = "FeatureCollection"
     featureColl['features'] = []

     prev_found = 0
     while (found != prev_found ):
       prev_found = found
       print(prev_found ,found)
       for node in G.nodes():
         if G.node[node]['lat'] == "null" and G.node[node]['lng'] == "null" and len(G.neighbors(node)) > 1: 
           neighbors[node] = []
           # find neighbours with coordinate
           for n in G.neighbors(node):
             if G.node[n]['lat'] != "null" and G.node[n]['lng'] != "null": 
               neighbors[node].append(n) 
           # TODO: check nodes with one neighbour 
           # if a point has more than two neighbours in the network 
           neiLen = len(neighbors[node])
           if neiLen >= 2:
             x1,y1 = proj1(G.node[neighbors[node][0]]['lat'],G.node[neighbors[node][0]]['lng'])
             x2,y2 = proj1(G.node[neighbors[node][1]]['lat'],G.node[neighbors[node][1]]['lng'])
             # r1 and r2, distances between node and the first two neighbours
             r1 = G[node][neighbors[node][0]]['length']
             r2 = G[node][neighbors[node][1]]['length']
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
               geometry = LineString([Point(newLat1,newLon1), Point(newLat2,newLon2)])#.buffer(0.001)
               geomCentroid = geometry.centroid
               buff = geomCentroid.buffer(0.05)
               # center of the line/buffer
               centerLat = geomCentroid.coords[0][0]
               centerLon = geomCentroid.coords[0][1]
               # line or buffer centroid as new coordinates, added to graph
               G.node[node]['lat'] = centerLat
               G.node[node]['lng'] = centerLon
               G.node[node]['status'] = "new"
               found = found - 1
               aFeature = {}
               aFeature['type'] = 'Feature'
               aFeature['geometry'] = {}
               aFeature['geometry']['type'] = 'Polygon'
               tmpCoords = []
               for coord in buff.exterior.coords:
                 tmpCoords.append([coord[0],coord[1]])
               aFeature['geometry']['coordinates'] = [tmpCoords]
               aFeature['properties'] = {}
               aFeature['properties']['name'] = node
               aFeature['properties']['centroid'] = mapping(buff.centroid)
               featureColl['features'].append(aFeature)
     # Write the buffers to file, together with the name of the toponym and possible coordinate, 
     #that is the centroid of the buffer and connecting line
     with open("../Data/newCoords_bufferCenter_circle.geojson", "w", encoding="utf8") as newCoordFile:
       json.dump(featureColl, newCoordFile, ensure_ascii=False, indent=4)
     # Write the new graph, contaning the new coordinates, into a file
     # To change the buffer between circular and ellipsoid, change the file name 
     featureColl['features'] = []
     for node in G.nodes():
       #if G.node[node]['lat'] != "null" and G.node[node]['lng'] != "null":
         aFeature = {}
         aFeature['type'] = 'Feature'
         aFeature['geometry'] = {}
         aFeature['geometry']['type'] = 'Point'
         aFeature['geometry']['coordinates'] = [G.node[node]['lat'], G.node[node]['lng']]
         aFeature['properties'] = {}
         aFeature['properties']['name'] = node
         aFeature['properties']['status'] = G.node[node]['status']
         featureColl['features'].append(aFeature)
     with open("../Data/newCoords_graph_bufferCenter_circle_withNullCoords.geojson", "w", encoding="utf8") as newGraph:
       json.dump(featureColl, newGraph, ensure_ascii=False, indent=4)
	
createGraph("../Data/tripleRoutes_withMeter2")


"""
Finds the closest points (from places.geojson) to start and end of each cornu route section

"""
import json
import csv
from json import load
import numpy
import math

class Point:
    def __init__(self, x, y, uri):
        self._x = x
        self._y = y
        self._uri = uri
    def dist_to_point(self, other):
        'Compute the Euclidean distance between two Point objects'
        delta_x = self._x - other._x
        delta_y = self._y - other._y
        return (delta_x ** 2 + delta_y ** 2) ** 0.5
    def __repr__(self):
        return '{:}, {:}, {:}'.format(self._x, self._y, self._uri)


def settlCoordinatesArray (placesFile):
  sttlArray = []
  with open(placesFile, 'r') as cornuFile:
            cornu = json.load(cornuFile)
            for cornuData in cornu['features']:
              lat = float(cornuData['properties']['cornuData']['coord_lat'])
              lon = float(cornuData['properties']['cornuData']['coord_lon'])
              uri = cornuData['properties']['cornuData']['cornu_URI']
              sttlArray.append(Point(lon, lat, uri))
  return sttlArray   
        
def newStartEndForRoutes(routesFile, sttlCoords, writeFile):
  matches = []
  notMatches = []
  firstPoint = sttlCoords[0]
  featureColl = {}
  featureColl['type'] = "FeatureCollection"
  featureColl['features'] = []    
  with open(routesFile) as rFile:    
      allData = json.load(rFile)
      for d in allData["features"]:
          '''aFeature = {}
          aFeature['type'] = 'Feature'
          aFeature['geometry'] = {}
          aFeature['geometry']['type'] = 'LineString'
          aFeature['geometry']['coordinates'] =
          aFeature['properties'] = {}
          aFeature['properties']['topType'] = d['topType']'''
          #lat, lon, and id from route section
          startPoint = Point( d["geometry"]["coordinates"][0][0], d["geometry"]["coordinates"][0][1], d["properties"]["sToponym"])
          closeToStart = firstPoint
          minToStart = startPoint.dist_to_point(closeToStart)
          endPoint = Point(d["geometry"]["coordinates"][-1][0], d["geometry"]["coordinates"][-1][1], d["properties"]["eToponym"])
          closeToEnd = firstPoint
          minToEnd = endPoint.dist_to_point(closeToEnd)
          for p in sttlCoords:
              tmpDist1 = startPoint.dist_to_point(p)
              tmpDist2 = endPoint.dist_to_point(p)
              if tmpDist1 < minToStart:
                closeToStart = p
                minToStart = tmpDist1
              if tmpDist2 < minToEnd:
                closeToEnd = p
                minToEnd = tmpDist2
          d['properties']['new_sToponym'] = closeToStart._uri
          d['properties']['new_eToponym'] = closeToEnd._uri
          d["geometry"]["coordinates"].insert(0, [closeToStart._x, closeToStart._y])
          d["geometry"]["coordinates"].append([closeToEnd._x, closeToEnd._y])  
          if startPoint._uri == closeToStart._uri and endPoint._uri == closeToEnd._uri:
            d['properties']['status'] = "match"
            matches.append((startPoint, minToStart, closeToStart, endPoint, minToEnd, closeToEnd)) 
          if startPoint._uri != closeToStart._uri or endPoint._uri != closeToEnd._uri:
            d['properties']['status'] = "notMatch"
            notMatches.append((startPoint, minToStart, closeToStart, endPoint, minToEnd, closeToEnd)) 
          featureColl['features'].append(d)
      with open(writeFile, 'w') as newCoordsFile:
          json.dump(featureColl, newCoordsFile, ensure_ascii=False, indent=4)  
  return matches, notMatches

  
sttls = settlCoordinatesArray("../../gazeteer/althurayya.github.io/master/places.geojson")

matches, notMatch = newStartEndForRoutes("../../gazeteer/althurayya.github.io/master/routes.json", sttls, "../Data/newRoutes.json")
print("all: ", len(matches), " not: ", len(notMatch))
with open("../Data/routes_matched", 'w', encoding="utf8") as f:
          writer = csv.writer(f, delimiter=',') 
          writer.writerow(["startPoint", "minToStart", "closeToStart", "endPoint", "minToEnd", "closeToEnd"])
          for r in matches:
            writer.writerow([r])
with open("../Data/routes_notMatches", 'w', encoding="utf8") as f:
          writer = csv.writer(f, delimiter=',') 
          writer.writerow(["startPoint", "minToStart", "closeToStart", "endPoint", "minToEnd", "closeToEnd"])
          for r in notMatch:
            writer.writerow([r])

print("All done!")


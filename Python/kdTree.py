import numpy as np
import json
from scipy.spatial import cKDTree

def settlCoordinatesArray (placesFile,routesFile):
  sttlArray = []
  startsArray =[]
  endsArray = []
  with open(placesFile, 'r') as cornuFile:
            cornu = json.load(cornuFile)
            for cornuData in cornu['features']:
              lat = float(cornuData['properties']['cornuData']['coord_lat'])
              lon = float(cornuData['properties']['cornuData']['coord_lon'])
              uri = cornuData['properties']['cornuData']['cornu_URI']
              sttlArray.append((lat, lon, uri))
  with open(routesFile, 'r') as cornuFile:
            cornu = json.load(cornuFile)
            for cornuData in cornu['features']:
              sLat = cornuData['geometry']['coordinates'][0][1]
              sLon = cornuData["geometry"]["coordinates"][0][0]
              eLat = cornuData['geometry']['coordinates'][-1][1]
              eLon = cornuData["geometry"]["coordinates"][-1][0]
              uri = cornuData['properties']['id']
              startsArray.append((sLat, sLon, uri))
              endsArray.append((eLat, eLon, uri))
  return sttlArray, startsArray, endsArray   

def main(sttls, starts, ends, routesFile):

# it will be much easier (and faster) to deal with numpy arrays here (you could
# always look up the corresponding node objects by index if you wanted to)
  X = np.array([(n[0], n[1]) for n in sttls])
  Y =  np.array([(n[0], n[1]) for n in starts]) 
  Z = np.array([(n[0], n[1]) for n in ends])
  #X = X.extend(Y)
  #X = X.extend(Z)
# construct a k-D tree
  tree = cKDTree(np.concatenate((X, Y, Z), axis=0))
  print(tree)
# query it with the first point, find the indices of all points within a maximum
# distance of 4.2 of the query point
  for p in Y:
    idx = tree.query(p)
    #	print(p, idx)

# these indices are one out from yours, since they start at 0 rather than 1
#print(idx)

sttlsArr, startsArr, endsArr = settlCoordinatesArray("../Data/places.geojson", "../Data/routes.json")
main (sttlsArr, startsArr, endsArr, "../Data/routes.json")

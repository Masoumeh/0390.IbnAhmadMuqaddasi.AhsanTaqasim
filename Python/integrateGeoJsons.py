# Split a big json to single geoJson files for each feature 

import json
from json import load
import os

def integrateJsonFiles(pathToFiles, writeFile):
  featureColl = {}
  featureColl['type'] = "FeatureCollection"
  featureColl['features'] = []
  for fileName in os.listdir(pathToFiles):
    with open(pathToFiles+fileName, "r", encoding="utf8") as singleFile:    
      data = json.load(singleFile)
      print("data: ",data["features"][0])
      featureColl['features'].append(data["features"][0])
  return featureColl

with open("../Data/all_data.geojson", 'w') as allFile:
     allData = integrateJsonFiles("../Data/places/", allFile)
     allFile.write(json.dumps(allData, indent=4,ensure_ascii=False))
print("done!")

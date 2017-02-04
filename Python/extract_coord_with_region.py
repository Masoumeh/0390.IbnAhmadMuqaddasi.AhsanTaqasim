"""
To extract coordinates and regions of sttl names of geographical text that are found in Cornu, using fuzzywuzzy library (or complete match commented!) and checking the region to which toponym belongs.
This scripts is initial and more complete functionalities is included in extract_coordWithHierarchy.py and then in extract_coordWithHierarchy_Normalized.py.
TODO: Incomplete!Needs to be completed.

"""
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from networkx.readwrite import json_graph

import io, json
import re
import sys 
import csv
from json import load
import global_var as gv


reload(sys)  
sys.setdefaultencoding('utf8')

def getSetOfSttl(fileName,name):
    """
    Finds the sttls from the hierarchy file (geographical text)
    """
    names = list()
    with open(fileName, "r") as f1:
        f1 = f1.read().split("\n")
        for l in f1:
          ls = l.split(",")
          #print(ls[-1])
          if ls[-1].startswith(name):
            names.append([ls[-1].strip('STTL').strip(' '),gv.reg_dict[ls[0].strip('PROV').strip(' ')]])
    print("name count: ", names)
    return names


def findCoord(cornuFile, name, fWriter):
  """
  Using the sttl names, find the coordinates from cornu and writes them into a csv file
  """
  coords = []
  with open(cornuFile) as jsonFile:    
    allData = json.load(jsonFile)
    for d in allData["features"]:
      fName = d["properties"]["cornuData"]["toponym_arabic"]
      sName = d["properties"]["cornuData"]["toponym_arabic"].split(",")
      region = d["properties"]["cornuData"]["region_code"]
#      if name == fName:
      # using fuzzywuzzy library
      if fuzz.ratio(name, fName) >= 90 and :
        fWriter.writerow([name, fName, sName[0], d["lat"], d["lon"], d["region"]])
      else:
        for n in sName:
#          if name == n.strip():
          # using fuzzywuzzy library
          if fuzz.ratio(name, n.strip()) >= 90:
            fWriter.writerow([name, fName, n.strip(), d["lat"], d["lon"], d["region"]])
            break


def getCornuSttlWithCoord(hierarchyFile, coordsFile):
    """
    The main function
    """
    global cnt
    data = []
    sttlNames = getSetOfSttl(hierarchyFile,"STTL")
    with open("../Data/STTLCoordsCSV_fuzzyWuzzy_with_Region", 'w') as csvCoord:
      fWriter = csv.writer(csvCoord, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
      fWriter.writerow(["geoTitle", "cornuName", "geoTitleOther", "lat", "lon", "cornuRegion"])
    
      for st in sttlNames:
        findCoord(coordsFile, st,fWriter)
           
      
getCornuSttlWithCoord("../Data/Shamela_0023696_Triples_H", "../Data/places.geojson")
print("Done!")  
    

from networkx.readwrite import json_graph
import io, json
import re
import sys 
import csv
from json import load


reload(sys)  
sys.setdefaultencoding('utf8')

def getSetOfSttl(fileName,name):
    names = list()
    with open(fileName, "r") as f1:
        f1 = f1.read().split("\n")
        for l in f1:
          ls = l.split(",")
          #print(ls[-1])
          if ls[-1].startswith(name):
            names.append(ls[-1].strip('STTL ').strip(' '))
    print("name count: ", len(names))
    return names


def findCoord(fileName, name, fWriter):
  coords = []
  with open(fileName) as jsonFile:    
    allData = json.load(jsonFile)
    for d in allData["data"]:
      fName = d["arTitle"]
      sName = d["arTitleOther"].split(",")
      if name == fName:
        fWriter.writerow([name, d["lat"], d["lon"], d["region"]])
      else:
        for n in sName:
          if name == n.strip():
            fWriter.writerow([name, d["lat"], d["lon"], d["region"]])

def getCornuSttlWithCoord(hierarchyFile, coordsFile):
    global cnt
    data = []
    sttlNames = getSetOfSttl(hierarchyFile,"STTL")
    #print(sttlNames)
    with open("STTLCoordsCSV", 'w') as csvCoord:
      fWriter = csv.writer(csvCoord, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
      fWriter.writerow(["name", "lat", "lon", "region"])
    
      for st in sttlNames:
        findCoord(coordsFile, st,fWriter)
           
      
getCornuSttlWithCoord("Shamela_0023696_Triples_H", "cornu_all_new.js")
print("Done!")  
    

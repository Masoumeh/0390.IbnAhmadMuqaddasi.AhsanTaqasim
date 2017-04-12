"""
Makes a list of similar sttl names with cornu, usinf fuzzywuzzy with more that 90% similarity ration (or exact match that is commented out!).
This is a version of extract_coordWithHierarchy.py extended with normalization function on arabic words. We use this script as the most complete version.
The output is a csv file, containing sttl names, region from both Cornu and geographical text and other information as:
["Title in geo text", "Name in Cornu", "TitleOther from Cornu", "lat", "lon", "belonging region in cornu", "Prov in geo text", "direct region (parent) in geo text", "eiSearch from Cornu", "translitTitle from Cornu"]
"""

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from networkx.readwrite import json_graph
import io, json
import re
import sys, codecs
import csv
from json import load
import normalization as norm


def getSttlWithRegs(fileName):
    """
    Makes a list of sttl names with region and province
    """
    # list of names together with latest region and province
    names = list()
    with open(fileName, "r", encoding="utf8") as f1:
        f1 = f1.read().split("\n")
        tmp = ""
        cnt = 0
        for l in f1:
          cnt = cnt + 1
          ls = l.split(",")
          if l:
            # join the sttl name with province to which it belongs
            tmp = "-".join((ls[-1][4:].strip(), ls[0][4:].strip(), ls[1][4:].strip()))
            #if tmp not in names:
            names.append(tmp)
            #else:
            #  print(tmp)
    print("name count: ", len(names))
    return names


def findCoord(fileName, sttlReg, fWriter):
  """
  Finds the coordinates, URI and the province belonging to for the sttls from cornu file
  and write them all together in a csv file.
  """

  sttlName = sttlReg.split('-')[0]
  with open(fileName, "r", encoding="utf8") as jsonFile:    
    allData = json.load(jsonFile)
    found = False
    for d in allData["features"]:
      fName = d["properties"]["cornuData"]["toponym_arabic"]
      sName = d["properties"]["cornuData"]["toponym_arabic_other"].split("،")
#      if name == fName:
      # check if it finds similar words with arTitle, using fuzzywuzzy library
      if sttlReg and fuzz.ratio(norm.normalizeArabic(sttlName), norm.normalizeArabic(fName))>= 90:
          found = True
#      if sttlReg and normalizeArabic(sttlName) == normalizeArabic(fName):
          fWriter.writerow([sttlName, sttlReg.split('-')[1], sttlReg.split('-')[2], fName, "/".join(sName), d["properties"]["cornuData"]["coord_lat"], d["properties"]["cornuData"]["coord_lon"], d["properties"]["cornuData"]["region_code"], d["properties"]["cornuData"]["cornu_URI"], fuzz.ratio(norm.normalizeArabic(sttlName), norm.normalizeArabic(fName))])

      else:
        for n in sName:
          n = n.strip()
#          if name == n.strip():
          # check if it finds similar words with arTitleOther, using fuzzywuzzy library
          if sttlReg and fuzz.ratio(norm.normalizeArabic(sttlName), norm.normalizeArabic(n))>= 90:
              found = True
#          if sttlReg and normalizeArabic(sttlName) == normalizeArabic(n):
              fWriter.writerow([sttlName, sttlReg.split('-')[1], sttlReg.split('-')[2], fName, "/".join(sName), d["properties"]["cornuData"]["coord_lat"], d["properties"]["cornuData"]["coord_lon"], d["properties"]["cornuData"]["region_code"],  d["properties"]["cornuData"]["cornu_URI"], fuzz.ratio(norm.normalizeArabic(sttlName), norm.normalizeArabic(n))])
              break

    if found == False:
        #print("last")
        fWriter.writerow([sttlName, sttlReg.split('-')[1], sttlReg.split('-')[2], "null", "null", "null", "null", "null", "null", 0])

def getCornuSttlWithCoord(hierarchyFile, coordsFile):
    sttlNames = getSttlWithRegs(hierarchyFile)
    with open("../Data/flat_geo_hierarchy_cornuMatches", 'w', encoding="utf8") as csvCoord:
      fWriter = csv.writer(csvCoord, delimiter=',', quoting=csv.QUOTE_MINIMAL)
      fWriter.writerow(["geoSttl", "geoProv", "geoReg1", "cornuTitle", "cornuTitleOther", "lat", "lon", "cornuRegion", "URI", "FW_ratio"])
      for st in sttlNames:
        findCoord(coordsFile, st, fWriter)
           
      
getCornuSttlWithCoord("../Data/flat_geo_hierarchy_H3", "../Data/places.geojson")
print("Done!")  
    

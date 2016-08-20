# Extracts the list of similar sttl names with cornu, using fuzzywuzzy and normalization (or exact match in comment!).
# Output file is csv, containing sttl names, region from both cornu and geography file. 

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from networkx.readwrite import json_graph
import io, json
import re
import sys, codecs
import csv
from json import load

# used for python 2.7
#reload(sys)  
#sys.setdefaultencoding('utf8')


# Normalization function
def normalizeArabic(text):
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ه", "ة", text)
    if text.startswith("ال"):
      text = text[2:] 
    return(text)

# makes a list of sttl names with region and provice
def getSttlWithRegs(fileName):
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
            # join the sttl name with latest region and province to which it belongs
            tmp = "-".join((ls[-1][4:].strip(), ls[0][4:].strip(), ls[-3][4:].strip()))
            #if tmp not in names:
            names.append(tmp)
            #else:
            #  print(tmp)
    print("name count: ", len(names))
    return names

# find the coordinates, last region and the province belonging to for the sttls from cornu file
# and write them all together in a file
def findCoord(fileName, sttlReg, fWriter):
  sttlName = sttlReg.split('-')[0]
  with open(fileName, "r", encoding="utf8") as jsonFile:    
    allData = json.load(jsonFile)
    for d in allData["data"]:
      fName = d["arTitle"]
      sName = d["arTitleOther"].split(",")
#      if name == fName:
      # check if it finds similar words with arTitle, using fuzzywuzzy library
      if sttlReg and fuzz.ratio(normalizeArabic(sttlName), normalizeArabic(fName))>= 90:
#      if sttlReg and normalizeArabic(sttlName) == normalizeArabic(fName):
          fWriter.writerow([sttlName, fName, "/".join(sName), d["lat"], d["lon"], d["region"], sttlReg.split('-')[1], sttlReg.split('-')[2], d["eiSearch"], d["translitTitle"], fuzz.ratio(normalizeArabic(sttlName), normalizeArabic(fName))])
      else:
        for n in sName:
          n = n.strip()
#          if name == n.strip():
          # check if it finds similar words with arTitleOther, using fuzzywuzzy library
          if sttlReg and fuzz.ratio(normalizeArabic(sttlName), normalizeArabic(n))>= 90:
#          if sttlReg and normalizeArabic(sttlName) == normalizeArabic(n):
              fWriter.writerow([sttlName, fName, n, d["lat"], d["lon"], d["region"], sttlReg.split('-')[1], sttlReg.split('-')[2], d["eiSearch"], d["translitTitle"], fuzz.ratio(normalizeArabic(sttlName), normalizeArabic(n))])
              break

def getCornuSttlWithCoord(hierarchyFile, coordsFile):
    sttlNames = getSttlWithRegs(hierarchyFile)
    with open("../Data/SttlReg_CoordsCSV_fuzzyWuzzy_normalized", 'w', encoding="utf8") as csvCoord:
      fWriter = csv.writer(csvCoord, delimiter=',', quoting=csv.QUOTE_MINIMAL)
      fWriter.writerow(["geoTitle", "cornuTitle", "cornuTitleOther", "lat", "lon", "cornuRegion", "geoProv", "geoFinalReg", "eiSearch", "translitTitle", "FW_ratio"])
      for st in sttlNames:
        findCoord(coordsFile, st, fWriter)
           
      
getCornuSttlWithCoord("../Data/Shamela_0023696_Triples_H", "../Data/cornu_all_new2.json")
print("Done!")  
    

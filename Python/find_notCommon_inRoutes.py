
from networkx.readwrite import json_graph
import io, json, csv
import re
import sys  


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

# makes a list of sttl names
def getSttlWithRegs(fileName):
    # list of names
    names = list()
    with open(fileName, "r", encoding="utf8") as f1:
        f1 = csv.reader(f1, delimiter=',')
        for l in f1:
          names.append(l[-1][4:].strip())
    return names

def findNotCommons(fileName):
    
   sttls = getSttlWithRegs("../Data/notCommon_checkAgainstCommons.txt")
   for sttl in sttls:
     with open(fileName, "r", encoding="utf8") as triRoutes:
       triRoutes = csv.reader(triRoutes, delimiter=',')
       for tri in triRoutes:
         #print("sttl:",sttl,"tri:",tri[0],"tri[1]:",tri[1],)
         if normalizeArabic(sttl) == normalizeArabic(tri[0].strip()) or normalizeArabic(sttl) == normalizeArabic(tri[1].strip()): 
           notCommonInRoutes.append(sttl)
   return notCommonInRoutes
    
findNotCommons("../Data/tripleRoutes_withMeter")


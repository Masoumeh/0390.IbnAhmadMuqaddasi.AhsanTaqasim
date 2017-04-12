"""
Create Matrix for cornu data in two levels (regions and setlements)
"""
import csv, json
import io
import numpy as np

def getRegions(data):
  regs = []
  topos = []
  for d in data["features"]:
    reg = d["properties"]["cornuData"]["region_code"]
    topoName = d["properties"]["cornuData"]["toponym_arabic"] +"، " + d["properties"]["cornuData"]["toponym_arabic_other"] 
    if reg not in regs:
      regs.append(reg)
    #if topoName not in topos and "RoutPoint" not in topoName:
    #  topos.append(topoName)
  return regs#, topos

def creatMatrixObj (fileName):
  with open(fileName, "r", encoding="utf8") as f1:
        f1 = json.load(f1)
        cols = getRegions(f1)
        newHierarchy = {}#[[0 for x in rows]  for y in range(len(cols))] 
        print("cols: ", cols)
        for data in f1["features"]:
            # Join the URI and all the names to form the values
            #toponym = (، ).join([data["properties"]["cornuData"]["cornu_URI"], data["properties"]["cornuData"]["toponym_arabic"], data["properties"]["cornuData"]["toponym_arabic_other"]])
            toponym = data["properties"]["cornuData"]["cornu_URI"]
            #skipStr = ("RoutPoint", "RoutePoint") #this is used for the commented value of toponym variable, checking routepoint in titles
            skipStr = ("ROUTPOINT", "ROUTEPOINT") #this is used for toponym which is just URI, checking routepoint in URI only
            if any(x in toponym for x in skipStr):
              continue
            reg = data["properties"]["cornuData"]["region_code"]
            if reg not in newHierarchy:
              newHierarchy[reg] = {}
            #if "cornu_"+reg not in newHierarchy:
              #newHierarchy["cornu_"+reg] = {}
           # if "ROUTPOINT" not in toponym:
            #newHierarchy["cornu_"+reg][toponym] = 1
            newHierarchy[reg][toponym] = 1
            #tmp = np.ma.array(cols, mask=False)
            #tmp.mask[reg] = True
            for r in cols:
              if r != reg:
                if r not in newHierarchy:
                  newHierarchy[r] = {}
                newHierarchy[r][toponym] = 0
                #if "cornu_"+r not in newHierarchy:
               #   newHierarchy["cornu_"+r] = {}
               # newHierarchy["cornu_"+r][toponym] = 0

  with open('../Data/matrix_cornu.json', 'w') as outfile:
        json.dump(newHierarchy, outfile, ensure_ascii=False, indent=4)


creatMatrixObj("../Data/places.geojson")
print("done!")

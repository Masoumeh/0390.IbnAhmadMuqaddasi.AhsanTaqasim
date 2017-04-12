"""
Create Matrix for Muqaddasi data in two levels (PROVs and STTLs)
"""
import csv, json
import io
import numpy as np
import global_var as gv

def getRegions(fileName):
  regs = []
  with open(fileName, "r", encoding="utf8") as f1:
    f1 = csv.reader(f1, delimiter=",")
    next(f1, None)  # skip the headers  regs = []
  #topos = []
    for d in f1:
      print(d)
      reg = d[1]
    #topoName = d[-1] 
      print(reg)
      if gv.reg_dict[reg] not in regs:
        regs.append(gv.reg_dict[reg])
    #if topoName not in topos and "RoutPoint" not in topoName:
    #  topos.append(topoName)
    print(regs)
  return regs#, topos

def createMatrixObj (fileName):
  cols = getRegions(fileName)
  with open(fileName, "r", encoding="utf8") as f1:
        f1 = csv.reader(f1, delimiter=",")
        next(f1, None)  # skip the headers
        #next(f1, None)  # skip the first extra row!
        newHierarchy = {}#[[0 for x in rows]  for y in range(len(cols))] 
        for line in f1:
            toponym = line[0]
            reg = gv.reg_dict[line[1]]
            #if "Muq_"+reg not in newHierarchy:
            #  newHierarchy["Muq_"+reg] = {}
            if reg not in newHierarchy:
              newHierarchy[reg] = {}
            if line[8] != "null":
              #toponym = (',').join([line[8], line[0], line[3], line[4]])
              toponym = line[8]
              #newHierarchy[reg][toponymList] = 1
            #else:
            #newHierarchy["Muq_"+reg][toponym] = 1
            newHierarchy[reg][toponym] = 1
            #tmp = np.ma.array(cols, mask=False)
            #tmp.mask[reg] = True
            for r in cols:
              if r != reg:
                #if "Muq_"+r not in newHierarchy:
                #  newHierarchy["Muq_"+r] = {}
                #newHierarchy["Muq_"+r][toponym] = 0
                if r not in newHierarchy:
                  newHierarchy[r] = {}
                newHierarchy[r][toponym] = 0

  with open('../Data/matrix_Muq_cornuMatches.json', 'w') as outfile:
        json.dump(newHierarchy, outfile, ensure_ascii=False, indent=4)
createMatrixObj("../Data/flat_geo_hierarchy_cornuMatches")
print("done!")

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
    #print(d)
      reg = d[0][4:].strip()
    #topoName = d[-1] 
      if reg not in regs:
        regs.append(gv.reg_dict[reg])
    #if topoName not in topos and "RoutPoint" not in topoName:
    #  topos.append(topoName)
    print(regs)
  return regs#, topos

def createMatrix (fileName):
  cols = getRegions(fileName)
  with open(fileName, "r", encoding="utf8") as f1:
        f1 = csv.reader(f1, delimiter=",")
        next(f1, None)  # skip the headers
        newHierarchy = {}#[[0 for x in rows]  for y in range(len(cols))] 
        for line in f1:
            toponym = line[-1][4:].strip()
            reg = line[0][4:].strip()
            if reg not in newHierarchy:
              newHierarchy[reg] = {}
            newHierarchy[reg][toponym] = 1
            #tmp = np.ma.array(cols, mask=False)
            #tmp.mask[reg] = True
            for r in cols:
              if r != reg:
                if r not in newHierarchy:
                  newHierarchy[r] = {}
                newHierarchy[r][toponym] = 0

  with open('../Data/matrix_Muq.json', 'w') as outfile:
        json.dump(newHierarchy, outfile, ensure_ascii=False, indent=4)
createMatrix("../Data/flat_geo_hierarchy")
print("done!")

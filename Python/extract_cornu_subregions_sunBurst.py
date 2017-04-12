'''
Create a json structure of cornu subregions (from initial json) suitable sunBurst chart
'''

import json

def build_cornu_subregs_sunburst(cornuFile, writeFile):
  with open(cornuFile) as jsonFile:    
      allData = json.load(jsonFile)
      subRegions = {}
      subRegions["name"] = "Cornu"
      subRegions["description"]= "Cornu Regions"
      subRegions["children"]= []
      for data in allData:
        tmp = {}
        tmp["name"] = data
        tmp["description"] = data
        tmp["children"] = []
        for child in allData[data]:
          chTmp = {}
          chTmp["name"] = child.split("، ")[0]
          chTmp["description"] = child
          chTmp["size"] = 1
          tmp["children"].append(chTmp) 
        subRegions["children"].append(tmp)        

  with open(writeFile, 'w') as cornuSubregs: 
    json.dump(subRegions, cornuSubregs, ensure_ascii=False, indent=4) 
   

build_cornu_subregs_sunburst("../Data/cornu_subRegs.json", "../Data/cornu_subRegs_sunBurst.json")
print("finished!")

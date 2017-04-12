'''
Extract subregions for each province in Muqaddasi
'''

'''
Create a json structure of cornu subregions (from initial json) suitable sunBurst chart
'''

import json

def build_muq_subregs_sunburst(cornuFile, writeFile):
  with open(cornuFile) as jsonFile:    
      allData = json.load(jsonFile)
      subRegions = {}
      subRegions["name"] = "Muqadasi"
      subRegions["description"]= "Muqaddasi Regions"
      subRegions["children"]= []
      for data in allData:
        tmp = {}
        tmp["name"] = data
        tmp["description"] = data
        tmp["children"] = []
        for child in allData[data]:
          chTmp = {}
          chTmp["name"] = child
          chTmp["description"] = child
          chTmp["size"] = 1
          tmp["children"].append(chTmp) 
        subRegions["children"].append(tmp)        

  with open(writeFile, 'w') as cornuSubregs: 
    json.dump(subRegions, cornuSubregs, ensure_ascii=False, indent=4) 
   

build_muq_subregs_sunburst("../Data/muq_subRegs.json", "../Data/muq_subRegs_sunBurst.json")
print("finished!")
        


print("finished!")

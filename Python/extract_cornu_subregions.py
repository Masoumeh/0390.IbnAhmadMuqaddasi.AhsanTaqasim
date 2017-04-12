'''
Extract subregions for each province in cornu
'''

import json

def find_cornu_subregs(cornuFile, writeFile):
  with open(cornuFile) as jsonFile:    
      allData = json.load(jsonFile)
      subRegions = {}
      for data in allData["features"]:
        #print(data)
        if data["properties"]["cornuData"]["region_code"] not in subRegions:
          subRegions[data["properties"]["cornuData"]["region_code"]] = []
        if data["properties"]["cornuData"]["top_type_hom"] == "regions":
          subRegions[data["properties"]["cornuData"]["region_code"]].append(data["properties"]["cornuData"]["toponym_arabic"] + "، " + data["properties"]["cornuData"]["toponym_arabic_other"])
  with open(writeFile, 'w') as cornuSubregs: 
    json.dump(subRegions, cornuSubregs, ensure_ascii=False, indent=4) 
        

find_cornu_subregs("../Data/places.geojson", "../Data/cornu_subRegs.json")
print("finished!")

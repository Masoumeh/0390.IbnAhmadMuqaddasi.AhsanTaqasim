'''
Extract subregions for each province in Muqaddasi
'''

import csv, json

def find_muq_subregs(muqFile, writeFile):
  with open(muqFile) as csvFile:    
      f1 = csv.reader(csvFile, delimiter=',')
      subRegions = {}
      for data in f1:
        prov = data[0][4:-1].strip()
        subreg = data[2][4:-1].strip()
        if prov not in subRegions:
          subRegions[prov] = []
        if subreg not in subRegions[prov]:
          subRegions[prov].append(subreg)
  with open(writeFile, 'w') as subregs: 
    json.dump(subRegions, subregs, ensure_ascii=False, indent=4) 
        

find_muq_subregs("../Data/Shamela_0023696_Triples_H3_H3", "../Data/muq_subRegs.json")
print("finished!")

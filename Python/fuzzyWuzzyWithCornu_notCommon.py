from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import io
import csv, json
import sys, re

reload(sys)  
sys.setdefaultencoding('utf8')

# To find common sttl names with cornu using fuzzywuzzy library.
# Can be replced with extract_coordWithHierarchy.py
sttls =[]
found = "false"
with open('../Data/Shamela_0023696_Triples_H', 'r') as csvfile:
  reader = csv.reader(csvfile, delimiter=',', quotechar='|')
  for row in reader:
      found == False
      sttl = row[-1][4:].strip()
      with open('../Data/cornu_all_new2.json') as cornu:    
        data = json.load(cornu)
        for d in data["data"]:
          if fuzz.ratio(d['arTitle'],sttl) >= 90:
            found = False
            for s in d['arTitleOther'].split(", "):#.split(' '+ u'xd8'):
              if fuzz.ratio(s,sttl) >= 90:
                found = True
                break;
          if found == True:
            break;
        if found == False:
          sttls.append(sttl) 

with io.open('../Data/fuzzyWuzzyWithCornu_notCommon.txt', 'w', encoding='utf-8') as f:
  f.write(unicode("\n".join(sttls))) 
print("done!") 

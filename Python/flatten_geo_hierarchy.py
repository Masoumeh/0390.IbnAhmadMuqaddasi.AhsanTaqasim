"""
To flatten the geo-Text hierarchy. We use Muqaddsi here
"""
import csv
import io
	
def flatten (fileName):
  with open(fileName, "r", encoding="utf8") as f1:
        f1 = csv.reader(f1, delimiter=",")
        newLines = []
        with open ("../Data/flat_geo_hierarchy_H3", 'w', encoding="utf8") as flatHier:
          fWriter = csv.writer(flatHier, delimiter=',', quoting=csv.QUOTE_MINIMAL)
          fWriter.writerow(["PROV", "REG1", "STTL"])
          for line in f1:
            if "STTL" in line[-1]:
              fWriter.writerow([line[0], line[2], line[-1]])

flatten("../Data/Shamela_0023696_Triples_H3_H3")
print("done!")

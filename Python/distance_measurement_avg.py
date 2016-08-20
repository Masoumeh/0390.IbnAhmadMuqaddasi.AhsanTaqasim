import re
import csv, json
# Average measurement for a distnce unit in geographical text

def measureAvgDistance(fileName):
    units = {}
    with open(fileName, 'r') as meterFile:
      distReader = csv.reader(meterFile, delimiter=',', quotechar='|')
      cnt = 0
      for dist in distReader:
          unit = dist[0][-1].strip()
          cnt = cnt+1
          distSum = []
          if unit in units:
            distSum.append(dist[-1])
            for d in distReader[cnt:]:
              u = d[0][-1].strip()
              if unit == u:
                distSum.append(d[-1])
          avg = sum(distSum)/len(distSum) if len(distSum) > 0 else float('nan')
          units[unit] = avg
      print(units)

measureAvgDistance("../Data/Shamela_Triples_Dist_cornuMeter")
print("Done!")

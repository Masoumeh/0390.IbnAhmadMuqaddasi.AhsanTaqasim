import re
import csv, json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# To find the related routes of toponyms which are not included %100 in cornu.
def extractRoutes(topoFile, routesFile, writer):
    with open(topoFile, "r", encoding="utf8") as notCommonsFile:
        notCommonsFile = notCommonsFile.read().split("\n")
        for nc in notCommonsFile:
          with open(routesFile, 'r') as geoRoutesFile:
            geoRoutes = csv.reader(geoRoutesFile, delimiter='\t', quotechar='|')
            #print("nc" , nc)
            for row in geoRoutes:
              #print("row0: ", row[0][5:].strip())
              #print("row1: ", row[1][5:].strip())
              if fuzz.ratio(nc,row[0][5:].strip())>= 90 or fuzz.ratio(nc,row[1][5:].strip())>= 90:
                writer.writerow(row)

with open("../Data/noCommon_Routes", "w", encoding="utf8") as distURI:
      fWriter = csv.writer(distURI, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
      fWriter.writerow(["From", "To", "originalDist"])
      extractRoutes("../Data/notCommon_checkAgainstCommons.txt", "../Data/Shamela_0023696_Triples_Dist", fWriter)
print("Done!")

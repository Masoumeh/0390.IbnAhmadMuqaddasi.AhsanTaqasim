"""
Extracts region, coords, and topURI for the route sections of a geographic text, all from Cornu.
It also uses some Arabic normalizations and on the word and fuzzywuzzzy function while searching and matching toponyms from both sources.
Matches also get checked 
For those toponyms in route sections (i.e. FROM/TO) which doesn't find any match in cornu, fills the information with "null" value.
The out put is a csv file, with all data lines of route sections (from geo text), extended as:
["From", "From_lat", "From_long", "From_Region(Cornu)", "From_URI(Cornu)", "To", "To_lat", "To_long", "To_Region(Cornu)", "To_URI", "original distance in classic text"]
"""
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from networkx.readwrite import json_graph
import io, json
import re
import sys, codecs
import csv
from json import load
import operator
import normalization as norm
import global_var as gv

# used for python 2.7
#reload(sys)  
#sys.setdefaultencoding('utf8')



def populateDict(string, region, data):
    """
    Populates a dictionay values with coordinates, region, and TOP_URI values for a toponym as key.
    used in getStartEndCoords function
    """
    found = False
    dictionary = {}
    string_norm = norm.normalizeArabic(string)
    fName = data["properties"]["cornuData"]["toponym_arabic"]
    fName_norm = norm.normalizeArabic(fName)
    sName = re.split('،|,',data["properties"]["cornuData"]["toponym_arabic_other"])
    cornu_reg = data["properties"]["cornuData"]["region_code"]
    key = ','.join([string] + region.strip().split(","))
    key_norm = ','.join([string_norm] + region.strip().split(","))

    if not any(x in dictionary for x in [key, key_norm]): 
      if (fuzz.ratio(string_norm , fName) >= 90 or fuzz.ratio(string , fName) >= 90 or any(x in [fName, fName_norm] for x in [string, string_norm])) and cornu_reg in region.strip().split(","):
        #print("key fName: ", string, "-", key)
        dictionary[key] = {}
        dictionary[key]['lat']= data["properties"]["cornuData"]["coord_lat"]
        dictionary[key]['lon'] = data["properties"]["cornuData"]["coord_lon"]
        dictionary[key]['region'] = data["properties"]["cornuData"]["region_code"]
        dictionary[key]['cornuUri'] = data["properties"]["cornuData"]["cornu_URI"]
        found = True

      else:
        for n in sName:
          if (fuzz.ratio(string_norm , n.strip()) >= 90 or fuzz.ratio(string , n.strip()) >= 90 or any(x in [n.strip(), norm.normalizeArabic(n.strip())] for x in [string, string_norm])) and cornu_reg in region.strip().split(","):
            #print("key sName: ", string, "-", key)
            dictionary[key] = {}
            dictionary[key]['lat']= data["properties"]["cornuData"]["coord_lat"]
            dictionary[key]['lon'] = data["properties"]["cornuData"]["coord_lon"]
            dictionary[key]['region'] = data["properties"]["cornuData"]["region_code"]
            dictionary[key]['cornuUri'] = data["properties"]["cornuData"]["cornu_URI"]
            found = True
            break

    '''if key not in dictionary and found == False: 
      #print("not in dic2: ", key)
      dictionary[key] = {}
      dictionary[key]['lat']= "null"
      dictionary[key]['lon'] = "null"
      dictionary[key]['region'] = region
      dictionary[key]['cornuUri'] = "null"'''
    return dictionary

def getStartEndCoords(fileName1, fileName2):
    """
    Extracts the coordinates, region, and URI for each toponym at start or end of a route section.
    The result is a dictionary with toponyms as key, and extracted data as values.
    It calls populateDict function to populate the dictionsry.
    """
    uniqueNames = dict()
    with open(fileName1, "r", encoding="utf8") as f1:
        f1 = csv.reader(f1, delimiter='\t')
        for ls in f1:
            start = ls[0][4:].strip()
            normStart = norm.normalizeArabic(start)
            start_reg = ls[1]#.strip().split(",")
            startKey = ','.join([normStart] + start_reg.strip().split(","))
            startKey_orig = ','.join([start] + start_reg.strip().split(","))
            end = ls[2][4:].strip()
            normEnd = norm.normalizeArabic(end)
            end_reg = ls[3]#.strip().split(",")
            endKey = ','.join([normEnd] + end_reg.strip().split(","))
            endKey_orig = ','.join([end] + end_reg.strip().split(","))

            with open(fileName2, "r", encoding="utf8") as jsonFile:    
              allData = json.load(jsonFile)
              for d in allData["features"]:
                # populates the uniqueNames dictionary for start and end toponyms
                if not any(x in uniqueNames for x in [startKey, startKey_orig]):
                  uniqueNames.update(populateDict(start, start_reg, d))
                if not any(x in uniqueNames for x in [endKey, endKey_orig]):
                  uniqueNames.update(populateDict(end, end_reg, d))
              if not any(x in uniqueNames for x in [startKey, startKey_orig]):
                  tmp = {}
                  tmp[startKey_orig] = {}
                  tmp[startKey_orig]['lat']= "null"
                  tmp[startKey_orig]['lon'] = "null"
                  tmp[startKey_orig]['region'] = start_reg
                  tmp[startKey_orig]['cornuUri'] = "null"
                  print("start: ", startKey_orig)
                  uniqueNames.update(tmp)

              if not any(x in uniqueNames for x in [endKey, endKey_orig]):
                  tmp = {}
                  tmp[endKey_orig] = {}
                  tmp[endKey_orig]['lat']= "null"
                  tmp[endKey_orig]['lon'] = "null"
                  tmp[endKey_orig]['region'] = end_reg
                  tmp[endKey_orig]['cornuUri'] = "null"
                  print("end: ", endKey_orig)
                  uniqueNames.update(tmp)  
        return uniqueNames


def getCornuCoord_forDistances(distanceFile, cornuCoordsFile):
    """
    The main function to create a structure and write it to a csv file.
    """
    dataToWrite = []
    not_common = []
    coords = getStartEndCoords(distanceFile,cornuCoordsFile)
    #print(coords)
    routes = {}
    #routes['data'] = []
    with open(distanceFile, "r", encoding="utf8") as csvfile:
        distances = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for line in distances:
          tmp = {}
          start = line[0][4:].strip()
          normStart = norm.normalizeArabic(start)
          startRegion = line[1].strip().split(",")
          startKey = ','.join([start] + startRegion).strip()
          startKey_norm = ','.join([normStart] + startRegion).strip()
          end = line[2][4:].strip()
          normEnd = norm.normalizeArabic(end)
          endRegion = line[3].strip().split(",")
          endKey = ','.join([end] + endRegion).strip()
          endKey_norm = ','.join([normEnd] + endRegion).strip()
          routes[startKey + "+" + endKey] = {}
          routes[startKey + "+" + endKey]['start'] = {}
          routes[startKey + "+" + endKey]['start']['URI'] = coords[startKey]['cornuUri'] if startKey in coords else coords[startKey_norm]['cornuUri']
          routes[startKey + "+" + endKey]['start']['lat'] = coords[startKey]['lat'] if startKey in coords else coords[startKey_norm]['lat']
          routes[startKey + "+" + endKey]['start']['lon'] = coords[startKey]['lon'] if startKey in coords else coords[startKey_norm]['lon']
          routes[startKey + "+" + endKey]['start']['region'] = coords[startKey]['region'] if startKey in coords else coords[startKey_norm]['region']
          routes[startKey + "+" + endKey]['end'] = {}
          routes[startKey + "+" + endKey]['end']['URI'] = coords[endKey]['cornuUri'] if endKey in coords else coords[endKey_norm]['cornuUri']
          routes[startKey + "+" + endKey]['end']['lat'] = coords[endKey]['lat'] if endKey in coords else coords[endKey_norm]['lat']
          routes[startKey + "+" + endKey]['end']['lon'] = coords[endKey]['lon'] if endKey in coords else coords[endKey_norm]['lon']
          routes[startKey + "+" + endKey]['end']['region'] = coords[endKey]['region'] if endKey in coords else coords[endKey_norm]['region']
          routes[startKey + "+" + endKey]['distance'] = line[-1][5:].strip()
          #routes['data'].append(tmp)
    with open('../Data/Distances_withCoords_normalized_with_cornuRegion_json_noNorm_noAL_origkey90', 'w') as outfile:
        json.dump(routes, outfile, ensure_ascii=False, indent=4)


getCornuCoord_forDistances("../Data/Shamela_0023696_Triples_Dist_with_Region", "../Data/places.geojson")
print("Done!")  
    

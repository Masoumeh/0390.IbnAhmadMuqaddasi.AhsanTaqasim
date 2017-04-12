"""
Extracts region, coords, and topURI for the route sections of a geographic text, all from Cornu.
It also uses some Arabic normalizations and on the word and fuzzywuzzzy function while searching and matching toponyms from both sources.
Matches also get checked 
For those toponyms in route sections (i.e. FROM/TO) which doesn't find any match in cornu, fills the information with "null" value.
The out put is a csv file, with all data lines of route sections (from geo text), extended as:
["From", "From_lat", "From_long", "From_Region(Cornu)", "From_URI(Cornu)", "To", "To_lat", "To_long", "To_Region(Cornu)", "To_URI", "original distance in classic text"]
"""
import csv
import json

from fuzzywuzzy import fuzz

from aratext import normalization as norm

# used for python 2.7
#reload(sys)  
#sys.setdefaultencoding('utf8')


'''def normalizeArabic(text):
    """
    Normalization function
    """
    text = re.sub("[إأٱآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ه", "ة", text)
    text = re.sub("ک", "ك", text)
    if text.startswith("ال"):
      text = text[2:] 
    return(text)'''


def populateDict(string, region, data):
    """
    Populates a dictionay values with coordinates, region, and TOP_URI values for a toponym as key.
    used in getStartEndCoords function
    """
    found = False
    dictionary = {}
    fName = data["properties"]["cornuData"]["toponym_arabic"]
    sName = data["properties"]["cornuData"]["toponym_arabic_other"].split(",")
    cornu_reg = data["properties"]["cornuData"]["region_code"]
    key = ','.join([norm.normalize_alphabet(string)] + region.strip().split(","))
    #print("region: ", region.strip().split(","))
    if key not in dictionary: 
      #print("not in dic1: ", key)
      if fuzz.ratio(norm.normalize_alphabet(string) , norm.normalize_alphabet(fName)) >= 90 and cornu_reg in region.strip().split(","):
        dictionary[key] = {}
        dictionary[key]['lat']= data["properties"]["cornuData"]["coord_lat"]
        dictionary[key]['lon'] = data["properties"]["cornuData"]["coord_lon"]
        dictionary[key]['region'] = data["properties"]["cornuData"]["region_code"]
        dictionary[key]['cornuUri'] = data["properties"]["cornuData"]["cornu_URI"]
        found = True
        #return dictionary
      else:
        for n in sName:
          if fuzz.ratio(norm.normalize_alphabet(string) , norm.normalize_alphabet(n.strip())) >= 90 and cornu_reg in region.strip().split(","):
            dictionary[key] = {}
            dictionary[key]['lat']= data["properties"]["cornuData"]["coord_lat"]
            dictionary[key]['lon'] = data["properties"]["cornuData"]["coord_lon"]
            dictionary[key]['region'] = data["properties"]["cornuData"]["region_code"]
            dictionary[key]['cornuUri'] = data["properties"]["cornuData"]["cornu_URI"]
            found = True
            break
            #return dictionary
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
            #print("ls: ", ls)
            start = ls[0][4:].strip()
            normStart = norm.normalize_alphabet(ls[0][4:].strip())
            start_reg = ls[1]#.strip().split(",")
            startKey = ','.join([normStart] + start_reg.strip().split(","))
            end = ls[2][4:].strip()
            normEnd = norm.normalize_alphabet(ls[2][4:].strip())
            end_reg = ls[3]#.strip().split(",")
            endKey = ','.join([normEnd] + end_reg.strip().split(","))
            #print("endreg: ", end_reg)
            with open(fileName2, "r", encoding="utf8") as jsonFile:    
              allData = json.load(jsonFile)
              for d in allData["features"]:
                # populates the uniqueNames dictionary for start and end toponyms
                if startKey not in uniqueNames:
                  uniqueNames.update(populateDict(start, start_reg, d))
                if endKey not in uniqueNames:
                  uniqueNames.update(populateDict(end, end_reg, d))
              if startKey not in uniqueNames:
                  #print("start: ", startKey)
                  tmp = {}
                  tmp[startKey] = {}
                  tmp[startKey]['lat']= "null"
                  tmp[startKey]['lon'] = "null"
                  tmp[startKey]['region'] = start_reg
                  tmp[startKey]['cornuUri'] = "null"
                  #print("tmpStart: ", tmp)
                  uniqueNames.update(tmp)
              if endKey not in uniqueNames:
                  #print("end: ", endKey)
                  tmp = {}
                  tmp[endKey] = {}
                  tmp[endKey]['lat']= "null"
                  tmp[endKey]['lon'] = "null"
                  tmp[endKey]['region'] = end_reg
                  tmp[endKey]['cornuUri'] = "null"
                  #print("tmpend ", tmp)
                  uniqueNames.update(tmp)  
                #print("endDic: ", uniqueNames)
        return uniqueNames


def getCornuCoord_forDistances(distanceFile, cornuCoordsFile):
    """
    The main function to create a structure and write it to a csv file.
    """
    dataToWrite = []
    not_common = []
    coords = getStartEndCoords(distanceFile,cornuCoordsFile)
    '''with open('../Data/uniqueNames', 'w') as outfile:
        json.dump(coords, outfile, ensure_ascii=False, indent=4)
    return
    routes = {}'''
    with open("../Data/Distances_withCoords_normalized_with_cornuRegion2", 'w', encoding="utf8") as csvCoord:
      fWriter = csv.writer(csvCoord, delimiter=',')
      fWriter.writerow(["From", "From_lat", "From_long", "From_Region", "From_URI", "To", "To_lat", "To_long", "To_Region", "To_URI", "distance"])
      with open(distanceFile, "r", encoding="utf8") as csvfile:
        distances = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for line in distances:
          start = line[0][5:].strip()
          normStart = norm.normalize_alphabet(line[0][5:].strip())
          startRegion = line[1].strip().split(",")
          startKey = ','.join([normStart] + startRegion).strip()
          end = line[2][5:].strip()
          normEnd = norm.normalize_alphabet(line[2][5:].strip())
          endRegion = line[3].strip().split(",")
          endKey = ','.join([normEnd] + endRegion).strip()
          distance = line[-1][5:].strip()
          #print(start, startRegion,  startKey,  end, endRegion, endKey)
          '''fWriter.writerow([start, ",".join( str(e) for e in coords[startKey]) if startKey in coords else "null","null",startRegion[0] if len(startRegion) > 1 else startRegion,"null", 
                            end, ",".join( str(e) for e in coords[endKey]) if endKey in coords else "null","null",endRegion[0] if len(endRegion) > 1 else endRegion,"null", distance])'''
          fWriter.writerow([start, coords[startKey]['lat'], coords[startKey]['lon'], coords[startKey]['region'], coords[startKey]['cornuUri'], 
                            end, coords[endKey]['lat'], coords[endKey]['lon'], coords[endKey]['region'], coords[endKey]['cornuUri'], distance])
        #fWriter.writerow(dataToWrite)
          '''if start not in coords:
             not_common.extend(start)
          if end not in coords:
             not_common.extend(end)
    with open("../Data/Distances_withoutCoords_normalized2", 'w', encoding="utf8") as f:
          writer = csv.writer(f, delimiter=',') 
          writer.writerow(["not_common"]) 
          for nc in not_common:
            writer.writerow([nc])'''

getCornuCoord_forDistances("../Data/Shamela_0023696_Triples_Dist_with_Region", "../Data/places.geojson")
print("Done!")  
    

"""
Replaces the classic distances with meter values. For example "عشرون مراحل" will be replaced by equivallent value in meters.
The calculations has been done before and here is available in a dictionary.
Tis script should be appended to check all the numerical values and units in original text. The values that we check here are just those mentioned in part of Al-Muqaddasi. 
Should eb generalized to include arbitrary units or numerical values.  
"""
import json
import re

from aratext import normalization as norm

pluralUnits = {"أيام": "يوم","مراحل": "مرحلة", "أميال":"ميل", "فراسخ": "فرسخ", "أنهر": "نهار", "أنهر": "نهارا", "ليال": "ليل", "مناهل": "يوم"}
unit_distance = {"يوما": 28156.0,"يوم": 28156.0, "بريدا": 17060.5, "فرسخا": 2888.2, "مرحلتين": 70357.0, "ميلا": 1941, "بريدين": 23504.153846153848,"مرحلة": 37987.00561797753, "يومين": 84568.0,"يومان": 84568.0,  "فرسخ": 2888.2, "بريد": 17060.5, "مرحلتان": 70357.0, "ميل": 1941, "نهار": 28156.0, "نهارا": 28156.0, "نهارين": 56312.0, "نصف نهار": 14078.0, "نهارا ونصفا": 42234, "منهلين":84568.0, "لیل": 7194, "ليلتان": 14388, "شهرا": 900000.0, "ليل": 7194}
numbers = {"نصف": 0.5,"واحد": 1,"إثنان":2,"ثلاثة":3,"ثلاثا":3,"ثلاث":3,"أربعة":4,"أربعا":4,"خمسة":5,"ستة":6,"سبعة":7,"ثمانية":8,"ثامن":8,"تسعة":9,"عشرة":10,"إحدى عشر":11,"إثنا عشر":12,"ثلاثة عشر":13,"أربعة عشر":14,"خمسة عشر":15,"ستة عشر":16,"سبعة عشر":17,"ثمانية عشر":18,"تسعة عشر":19,"عشرون":20,"واحد وعشرون":21,"إثنان وعشرون":22,"ثلاثة وعشرون":23,"أربعة وعشرون":24,"أربع وعشرين":24,"أربع وعشرون":24,"خمسة وعشرون":25,"ستة وعشرون":26,"سبعة وعشرون":27,"ثمانية وعشرون":28,"تسعة وعشرون":29,"ثلاثون":30,"واحد وثلاثون":31, "عشرين":20,"واحد وعشرين":21,"إثنان وعشرين":22,"ثلاثة وعشرين":23,"أربعة وعشرين":34,"خمسة وعشرين":25,"ستة وعشرين":26,"سبعة وعشرين":27,"ثمانية وعشرين":28,"تسعة وعشرين":29,"ثلاثين":30,"واحد وثلاثين":31, "إثنان وثلاثون":32, "إثنان وثلاثين":32 ,"ثلاثة وثلاثين":33 , "ثلاثة وثلاثون":33, "أربعة وثلاثين":34, "أربعة وثلاثون":34, "أربع وثلاثين":34, "أربعة وثلاثون":34, "خمسة وثلاثين": 35, "خمسة وثلاثون": 35, "سبعة وثلاثين": 37, "ستة وثلاثون": 36, "ستة وثلاثون": 36, "سبعة وثلاثون": 37, "ثمانية وثلاثين": 38, "ثمانية وثلاثون": 38, "تسعة وثلاثين": 39, "تسعة وثلاثون": 39, "أربعون":40, "اثنان وأربعون": 42, "واحد وأربعون": 41, "ثمانية وأربعون": 48,  "ثمانية وأربعون": 48, "خمسون": 50,"خمسين": 50,"ستين": 60,"ستون": 60, "سبعون": 70,"سبعين": 70,"أربعة وسبعين": 74,"أربعة وسبعون": 74,"ثمانين": 80, "ثلاثمائة": 3000, "الفين ومائة وخمسين": 2150} 

def replaceUnitsWithMeter(fileName):
    """
    Checks the classic values with the given map (from classic to modern values) and replace them as distances in meter for route sections.
    """
    normalized_number = {}
    normalized_unit_distance = {}
    normalized_pluralUnits = {}
    
    for k in numbers:
      normalized_number[norm.normalize_alphabet(k)] = numbers[k]
    for k in unit_distance:
      normalized_unit_distance[norm.normalize_alphabet(k)] = unit_distance[k]
    for k in pluralUnits:
      normalized_pluralUnits[norm.normalize_alphabet(k)] = pluralUnits[k]

    excluded_routes = []
    routes = {}
    with open(fileName, 'r') as meterFile:
      distReader = json.load(meterFile)
      for row in distReader:
          dist = distReader[row]['distance'].strip()
          splitDist = dist.split(' ')
          if len(splitDist) == 1:
            if splitDist[0] in unit_distance or norm.normalize_alphabet(splitDist[0]) in normalized_unit_distance:
              meter = normalized_unit_distance[norm.normalize_alphabet(splitDist[0])]
              distReader[row]['cornu_meter'] = meter
              routes[row] = distReader[row]
              #writer.writerow([row[0], row[1], row[2], row[3].strip('"'), row[4], row[5], row[6], row[7], row[8].strip('"'), row[9], row[10], meter])
            else:
              distReader[row]['cornu_meter'] = "null"
              routes[row] = distReader[row]
              #writer.writerow([row[0], row[1], row[2], row[3].strip('"'), row[4], row[5], row[6], row[7], row[8].strip('"'), row[9], row[10], "null"])
          elif len(splitDist) > 1:
            if re.search('[0-9]', splitDist[0]):
              if norm.normalize_alphabet(splitDist[1]) in normalized_unit_distance or splitDist[1] in unit_distance:
                meter = float(norm.normalize_alphabet(splitDist[0])) * normalized_unit_distance[norm.normalize_alphabet(splitDist[1])]
                distReader[row]['cornu_meter'] = meter
                routes[row] = distReader[row]
                
              elif norm.normalize_alphabet(splitDist[1]) in normalized_pluralUnits or splitDist[1] in pluralUnits:
                single_unit = normalized_pluralUnits[norm.normalize_alphabet(splitDist[1])]
                meter = float(norm.normalize_alphabet(splitDist[0])) * normalized_unit_distance[single_unit]
                distReader[row]['cornu_meter'] = meter
                routes[row] = distReader[row]
              else:
                distReader[row]['cornu_meter'] = "null"
                routes[row] = distReader[row]
                
            else:
              unit = next((y for y in splitDist if (y in unit_distance or y in pluralUnits or y in normalized_unit_distance or y in normalized_pluralUnits)), None)
              if unit != None:
                unit_index = splitDist.index(unit)
                value = ' '.join(splitDist[:unit_index])
                if norm.normalize_alphabet(value) in normalized_number or value in numbers:
                  multiplyValue = normalized_number[norm.normalize_alphabet(value)]
                  if norm.normalize_alphabet(splitDist[unit_index]) in normalized_pluralUnits or splitDist[unit_index] in pluralUnits:
                    single_unit = normalized_pluralUnits[norm.normalize_alphabet(splitDist[unit_index])]
                    meter = normalized_number[norm.normalize_alphabet(value)] * normalized_unit_distance[single_unit]
                    distReader[row]['cornu_meter'] = meter
                    routes[row] = distReader[row]

                  elif norm.normalize_alphabet(splitDist[unit_index]) in normalized_unit_distance or splitDist[unit_index] in unit_distance:
                    meter = normalized_number[norm.normalize_alphabet(value)] * normalized_unit_distance[norm.normalize_alphabet(splitDist[unit_index])]
                    distReader[row]['cornu_meter'] = meter
                    routes[row] = distReader[row]
                    
                  else:
                    distReader[row]['cornu_meter'] = "null"
                    routes[row] = distReader[row]
                    
                else: 
                  distReader[row]['cornu_meter'] = "nul"
                  routes[row] = distReader[row]
                  
              else:
                distReader[row]['cornu_meter'] = "null"
                routes[row] = distReader[row]
                
          else:
            distReader[row]['cornu_meter'] = "null"
            routes[row] = distReader[row]

    with open("../Data/tripleRoutes_withMeter2_normalized_with_cornuRegion_json_noNorm_noAL_origkey90", "w", encoding="utf8") as distMeter:
      json.dump(routes, distMeter, ensure_ascii=False, indent=4)

replaceUnitsWithMeter("../Data/Distances_withCoords_normalized_with_cornuRegion_json_noNorm_noAL_origkey90")
print("Done!")

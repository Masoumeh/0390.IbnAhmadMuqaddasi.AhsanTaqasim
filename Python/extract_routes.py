"""
To extract route sections in triples from a tagged text. 
This script is written seperalt from extract_data (and maybe extract_hierarchy if it's written) to extract the region for each route section as well.
The output is a csv file, each line holding triples (FROM, From_REG, TO, TO_REG, DIST)
TODO: New script for transliting the Arabic regions names 
"""

import re
import global_var as gv

def extractTriples(fileName):
    """
    The main function to extract route sections (with countries/Eqlima) 
    """
    '''reg_dict = {"جزيرة العرب": "Jazirat al-Arab,Yemen", "إقليم العراق": "Iraq", "إقليم أقور": "Aqur", "إقليم الشام": "Sham", "إقليم مصر": "Egypt", "إقليم المغرب": "Maghrib,Barqa,Andalus", "ذكر بادية العرب": "Badiyat al-Arab", "إقليم السند": "Sind", "إقليم كرمان": "Kirman", "إقليم فارس": "Faris", "إقليم خوزستان": "Khuzistan", "إقليم الجبال": "Jibal", "إقليم الرحاب": "Rihab", "إقليم الديلم": "Daylam", "إقليم المشرق": "Khurasan,Sijistan,Transoxiana"}'''
    data = []
    with open(fileName, "r", encoding="utf8") as f1:
        f1 = f1.read().split("\n")
        # initial value for region which will be changed when a new section is started with "### |" tag
        region = ""
        print(gv.reg_dict)
        for l in f1:
          if re.match(r'### \| [\u0600-\u06FF]+', l):
            region = l[6:].strip()
          # process lines starting with route section tags
          elif l.startswith("#$#FROM"):
                l = l.split("#$#")[1:]

                dist = l[2]
                distTag = dist[:4]
                #distVal = val[4:].split("#")

                #for v in vals:
                newValue = "\t".join([l[0], gv.reg_dict[region], l[1], gv.reg_dict[region], dist])
                data.append(newValue)

        with open("../Data/" + fileName + "_Triples_Dist_with_Region", "w", encoding="utf8") as f9:
            f9.write("\n".join(data))


extractTriples("../Data/Shamela_0023696")
print("Done!")

import csv
import re
import global_var as gv

def extract_tri_route(input_file, out_file):
    """
    To extract route sections data in triples from a tagged text.
    This is the first script to get the data out of a text.
    The output is a csv file, each line holding triples (FROM, TO, DIST)
    :param input_file: The given file
    :return:
    """
    data = []
    tmp_tri = []
    with open(input_file, "r", encoding="utf8") as f1:
        f1 = f1.read().split("\n")
        for l in f1:
            # to include distances in extraction, remove PROV and REG strings in the below line
            if l.startswith("#$#FROM"):
            # if l.startswith("#$#PROV") or l.startswith("#$#REG"):
                l = l.split("#$#")[1:]
                print(l)
                val = l[2]
                valTag = val[:4]
                vals = val[4:].split("#")

                for v in vals:
                    tmp_tri = [l[0], l[1], valTag + v]
                    data.append(tmp_tri)

    with open(out_file, "w", encoding="utf8") as out_file:
        headers = ["from", "to", "distance"]
        # headers = ["from", "to"]
        writer = csv.DictWriter(out_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
        writer.writeheader()
        for d in data:
            writer.writerow({'from': d[0][4:].strip(),
                             'to': d[1][4:].strip(),
                             'distance': d[-1][4:].strip()})

def extract_tri_hier(input_file, out_file):
    """
    To extract hierarchical data in triples from a tagged text.
    This is the first script to get the data out of a text.
    The output is a csv file, each line holding triples (REG/PROV, TYPE, REG/STTL)
    :param input_file: The given file
    :return:
    """
    data = []
    tmp_tri = []
    with open(input_file, "r", encoding="utf8") as f1:
        f1 = f1.read().split("\n")
        for l in f1:
            # to include distances in extraction, remove PROV and REG strings in the below line
            if l.startswith("#$#PROV") or l.startswith("#$#REG"):
                l = l.split("#$#")[1:]
                # print(l)
                val = l[2]
                val_tag = val[:4]
                vals = val[4:].split("#")

                for v in vals:
                    tmp_tri = [l[0], l[1], val_tag + v]
                    data.append(tmp_tri)

    with open(out_file, "w", encoding="utf8") as out_file:
        # headers = ["from", "to", "distance"]
        writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for d in data:
            writer.writerow([d[0][4:].strip(), d[1][4:].strip(), d[-1][4:].strip()])


"""
To extract route sections in triples from a tagged text. 
This script is written seperalt from extract_data (and maybe extract_hierarchy if it's written) to extract the region for each route section as well.
The output is a csv file, each line holding triples (FROM, From_REG, TO, TO_REG, DIST)
TODO: New script for transliting the Arabic regions names 
"""


def extract_route_wReg(input_file, out_file, starting_tag):
    """
    The main function to extract route sections (with countries/Eqlima) 
    """
    '''reg_dict = {"جزيرة العرب": "Jazirat al-Arab,Yemen", "إقليم العراق": "Iraq", "إقليم أقور": "Aqur", "إقليم الشام": "Sham", "إقليم مصر": "Egypt", "إقليم المغرب": "Maghrib,Barqa,Andalus", "ذكر بادية العرب": "Badiyat al-Arab", "إقليم السند": "Sind", "إقليم كرمان": "Kirman", "إقليم فارس": "Faris", "إقليم خوزستان": "Khuzistan", "إقليم الجبال": "Jibal", "إقليم الرحاب": "Rihab", "إقليم الديلم": "Daylam", "إقليم المشرق": "Khurasan,Sijistan,Transoxiana"}'''
    data = []
    with open(input_file, "r", encoding="utf8") as f1:
        f1 = f1.read().split("\n")
        # initial value for region which will be changed when a new section is started with "### |" tag
        region = ""
        print(gv.reg_dict)
        for l in f1:
          #   check against the section header
          if re.match(r'### \| [\u0600-\u06FF]+', l):
            region = l[5:].strip()
          # process lines starting with route section tags
          elif l.startswith(starting_tag):
                l = l.split("#$#")[1:]

                val = l[2]
                val_tag = val[:4]
                vals = val[4:].split("#")

                for v in vals:
                    tmp_tri = [l[0], gv.reg_dict[region], l[1], gv.reg_dict[region], val_tag + v]
                    data.append(tmp_tri)

    with open(out_file, "w", encoding="utf8") as out_file:
        # headers = ["from", "to", "distance"]
        writer = csv.writer(out_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for d in data:
            writer.writerow([d[0][4:].strip(), d[1], d[2][4:].strip(), d[3], d[-1][4:].strip()])



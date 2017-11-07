import get_matches as gm
import codecs
import pandas as pan
from itertools import *
import csv
import os.path

write_file = "/home/rostam/Desktop/Chiara/itiTopos_trismegis_matches"
topos_file = "/home/rostam/Desktop/Chiara/It.Ant. - tagged_new_itiTopos"
matching_file = "/home/rostam/Desktop/Chiara/Trismegistos_matchings"
pleiades_file = "/home/rostam/Desktop/Chiara/pleiades_matchings.csv"

file_exists = os.path.isfile(write_file)

with open(matching_file, "r", encoding="utf8") as matches:
    rows = pan.read_csv(matches, delimiter='\t', names=["Node", "Trismegistos_Names", "Neighbours", "Status", "Method"])
    with open(write_file, 'a', encoding="utf8") as matches_file:
        headers = ["Node", "Pleiades title", "Node Region", "Pleiades id", "Geometry", "Status", "Method"]
        writer = csv.DictWriter(matches_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
        if not file_exists:
            writer.writeheader()  # write a header if the file does not exist
        with open(topos_file, "r", encoding="utf8") as topos:
            tops = topos.readlines()
            with open(pleiades_file, "r", encoding="utf8") as pleiades:
                pleiades_matches = pan.read_csv(pleiades, delimiter='\t',
                                        names=["Node", "Pleiades title", "Node Region",
                                           "Pleiades id", "Geometry", "Status", "Method"])
                for t in tops:
                    # print("t: ",t.strip())
                    for index, match in islice(rows.iterrows(), 1, None):
                        if match["Node"] == t.strip() and match["Status"] == "Exact":
                            for i,plei_match in islice(pleiades_matches.iterrows(),1,None):
                                if str(match["Trismegistos_Names"]).split("-")[1].split("(")[0].strip() == \
                                        plei_match["Node"].strip():
                                    print(plei_match["Node"])
                                    writer.writerow({"Node": plei_match["Node"], "Pleiades title":plei_match["Pleiades title"],
                                                         "Node Region": plei_match["Node Region"],
                                                         "Pleiades id": plei_match["Pleiades id"], "Geometry":plei_match["Geometry"],
                                                         "Status": plei_match["Status"], "Method": plei_match["Method"]})


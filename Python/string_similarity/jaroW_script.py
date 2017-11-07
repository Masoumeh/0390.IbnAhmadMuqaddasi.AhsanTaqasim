import get_sttl_reg as sttl
import get_matches as gm
import match_functions as mf
import csv
import pandas as pan
from graph import create_graph as cg

input_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/string_similarity/match_results_evaluated"
hier_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_hier_all"
cornu_places = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/places.geojson"

matches = {}

f1 = open(input_file, "r")
found_topos = set()
sttl_reg_set = sttl.get_sttl_with_reg(hier_file)
cornu_graph = cg.create_graph_geojson("../../Data/routes.json", "../../Data/places_new_structure.geojson")
found_file = pan.read_csv(f1, delimiter='\t', names=["Geo Title", "Cornu Title", "Cornu Title Other",
            "lat", "lon", "Cornu Region", "Geo Prov", "Geo Subregion", "Cornu URI", "Status", "Match Method"])
cornu_topos_matched = set()
for index, row in found_file.iterrows():
    # print(row)
    if row["Status"] == "exact":
        if row["Match Method"] not in matches:
            matches[row["Match Method"]] = 0
        matches[row["Match Method"]] += 1
        found_topos.add(row["Geo Title"].strip() + "/" + row["Geo Prov"].strip() + "/" + row["Geo Subregion"].strip())
        cornu_topos_matched.add(row["Cornu URI"])
not_found_topos = [item for item in sttl_reg_set if item not in found_topos]
print("found: ", len(found_topos))
print("not: ", not_found_topos)
# print(matches)
gm.get_cornu_matches(not_found_topos, cornu_places,
                     #cornu_graph,
                     input_file, mf.cosine_match,
                     "NA", "cosine", cornu_topos_matched)
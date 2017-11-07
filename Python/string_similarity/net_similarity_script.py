import get_sttl_reg as sttl
import get_matches as gm
import match_functions as mf
import csv
import pandas as pan
import codecs
from graph import create_graph as cg


input_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/string_similarity/match_results_exact_routes"
cornu_places = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/places.geojson"
routes_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_triples_route_wReg"

f1 = codecs.open(input_file, "r",encoding='utf-8', errors='ignore')
found_topos = set()
sttl_reg_set = cg.create_graph_csv(routes_file)
g_cornu = cg.create_graph_geojson("../../Data/routes.json", "../../Data/places_new_structure.geojson")

found_file = pan.read_csv(f1, delimiter='\t', names=["Geo Title", "Cornu Title", "Cornu Title Other", 'Geo Neighbours', 'Cornu Neighbours', "lat", "lon", "Cornu Region", "Geo Prov",
                   "Geo Subregion", "Cornu URI", "Status", "Match Method"])
cornu_topos_matched = set()
eval_list = []
# print("g: ", sttl_reg_set.nodes())
matches = {}
for index, row in found_file.iterrows():
    if row["Status"] == "exact":
        if row["Match Method"] not in matches:
            matches[row["Match Method"]] = 0
        matches[row["Match Method"]] += 1
        tmp = row["Geo Title"] + "/" + row["Geo Prov"]
        if tmp in sttl_reg_set:
            sttl_reg_set.node[tmp]['matches'].append(row['Cornu URI'])
        # print(sttl_reg_set.node[tmp]['matches'])
        found_topos.add(tmp)
        # cornu_topos_matched.add(row["Cornu URI"])
# sttl_list = [s for s in sttl_reg_set.nodes() if len(sttl_reg_set.node[s]['matches']) == 0]
# for hier data
not_found_topos = [item for item in sttl_reg_set.nodes() if item not in found_topos]
cornu_topos_matched = set()
print(len(found_topos))
print(len(not_found_topos))
print(matches)
# gm.get_cornu_matches(sttl_reg_set, cornu_places, g_cornu, input_file, mf.dice_match,
#                      "NA", "Dice", cornu_topos_matched)
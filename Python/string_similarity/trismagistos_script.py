import get_matches as gm
from graph import create_graph as cg
import codecs
import pandas as pan
from itertools import *


input_file = "/home/rostam/Desktop/Chiara/Trismegistos_matchings"
routes_file = "/home/rostam/Desktop/Chiara/It.Ant. - tagged_new_tri"
pleiades_places = "/home/rostam/Desktop/Chiara/pleiades-places.json"
trismegis_places = "/home/rostam/Desktop/Chiara/Trismegistos_georefsearch_2017_08_28.csv"
g_txt = cg.create_graph_csv(routes_file)
matches = {}
f1 = codecs.open(input_file, "r", encoding='utf-8', errors='ignore')
found_topos = set() # should be empty for exact matches run for the first time
# sttl_reg_set = sttl.get_sttl_with_reg(hier_file)
found_file = pan.read_csv(f1, delimiter='\t', names=["Node", "Trismegistos_Names", "Neighbours", "Status", "Method"])
tris_topos_matched = set()
eval_list = []
na = 0
for index, row in islice(found_file.iterrows(), 1, None):
    if row["Status"] == "Exact":
        # na += 1
        # if row["Method"] not in matches:
        #     matches[row["Method"]] = 0
        # matches[row["Method"]] += 1
        # tmp = row["Geo Title"] + "-" + row["Geo Prov"] + "-" + row["Geo Subregion"]
        found_topos.add(row["Node"])
        # tris_topos_matched.add(row["Trismegistos_Names"])
not_found_topos = [item for item in g_txt.nodes() if item not in found_topos]
print(na)
print(len(found_topos))
print(len(not_found_topos))
print(len(g_txt.nodes()))
print(matches)
# for node in g_txt.nodes():
#     if node == "Exploratione":
#         print(g_txt.neighbors(node))
# gm.get_pleiades_matches(g_txt, pleiades_places, routes_file, input_file)
gm.get_trismegi_matches(g_txt, found_topos, trismegis_places, input_file)
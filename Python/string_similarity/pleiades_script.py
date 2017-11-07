import get_matches as gm
from graph import create_graph as cg
import codecs
import pandas as pan
from itertools import *


input_file = "/home/rostam/Desktop/Chiara/pleiades_matchings"
tris_file = "/home/rostam/Desktop/Chiara/Trismegistos_matchings"
# nodes_file = "/home/rostam/Desktop/Chiara/"
routes_file = "/home/rostam/Desktop/Chiara/It.Ant. - tagged_new_tri"
pleiades_places = "/home/rostam/Desktop/Chiara/pleiades-places.json"
trismegis_places = "/home/rostam/Desktop/Chiara/Trismegistos_georefsearch_2017_08_28.csv"
g_txt = cg.create_graph_csv(routes_file)
matches = {}
f1 = codecs.open(tris_file, "r", encoding='utf-8', errors='ignore')
found_topos = set() # should be empty for exact matches run for the first time
# sttl_reg_set = sttl.get_sttl_with_reg(hier_file)
found_file = pan.read_csv(f1, delimiter='\t', names=["Node", "Trismegistos_Names", "Neighbours", "Status", "Method"])
tris_topos_matched = set()
eval_list = []
tris_names = []
for index, row in islice(found_file.iterrows(), 1, None):
    if row["Status"] == "Exact":
        tris_names.append(str(row["Trismegistos_Names"]).split(",")[0])#.split(" - ")[1].split("(")[0].strip())
# print(tris_names)
# print(len(tris_names))
gm.get_pleiades_matches(tris_names, pleiades_places, input_file)
# gm.get_trismegi_matches(g_txt, found_topos, trismegis_places, input_file)
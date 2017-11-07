import get_sttl_reg as sttl
import get_matches as gm
import match_functions as mf
import pandas as pan
from graph import create_graph as cg


input_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/string_similarity/match_results_evaluated"
out_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/string_similarity/tmp_leven_matches"
hier_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_hier_all"
cornu_places = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/places.geojson"

f1 = open(input_file, "r")
found_topos = set()
sttl_reg_set = sttl.get_sttl_with_reg(hier_file)
found_file = pan.read_csv(f1, delimiter='\t', names=["Geo Title", "Cornu Title", "Cornu Title Other",
                                                     "lat", "lon", "Cornu Region", "Geo Prov",
                                                     "Geo Subregion", "Cornu URI", "Status",
                                                     "Match Method"])
cornu_topos_matched = set()
# g_cornu = cg.create_graph_geojson("../../Data/routes.json", "../../Data/places_new_structure.geojson")

for index, row in found_file.iterrows():
    # print(row)
    if row["Status"] == "exact":
        found_topos.add(row["Geo Title"] + "/" + row["Geo Prov"] + "/" + row["Geo Subregion"])
        cornu_topos_matched.add(row["Cornu URI"])
not_found_topos = [item for item in sttl_reg_set if item not in found_topos]
for nf in not_found_topos:
    print(nf)
print(len(cornu_topos_matched))
print(len(found_topos))
print(len(not_found_topos))
gm.get_cornu_matches(not_found_topos, cornu_places, input_file, mf.dam_levenstein_match,
                     "NA", "Dam Levenstein", cornu_topos_matched)
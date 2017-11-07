import get_sttl_reg as sttl
import get_matches as gm
import match_functions as mf
import csv
import pandas as pan
import codecs


input_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/string_similarity/match_results_evaluated"
hier_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_hier_all"
cornu_places = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/places.geojson"

f1 = codecs.open(input_file, "r",encoding='utf-8', errors='ignore')
found_topos = set()
sttl_reg_set = sttl.get_sttl_with_reg(hier_file)
found_file = pan.read_csv(f1, delimiter='\t', names=["Geo Title", "Cornu Title", "Cornu Title Other",
                                                     "lat", "lon", "Cornu Region", "Geo Prov",
                                                     "Geo Subregion", "Cornu URI", "Status",
                                                     "Match Method"])
cornu_topos_matched = set()
eval_list = []
for index, row in found_file.iterrows():
    if row["Status"] == "exact":
        tmp = row["Geo Title"] + "-" + row["Geo Prov"] + "-" + row["Geo Subregion"]
        found_topos.add(tmp)
        cornu_topos_matched.add(row["Cornu URI"])
not_found_topos = [item for item in sttl_reg_set if item not in found_topos]
print(len(found_topos))
print(len(not_found_topos))
# gm.get_cornu_matches(not_found_topos, cornu_places, input_file, mf.dam_levenstein_match,
#                      "NA", "Dam Levenstein", cornu_topos_matched)
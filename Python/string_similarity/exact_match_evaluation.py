import get_sttl_reg as sttl
import get_matches as gm
import match_functions as mf
import csv
import pandas as pan


input_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/string_similarity/match_results_new_exact2"
hier_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_hier_all"
cornu_places = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/places.geojson"
exact_evaluation = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/string_similarity/exact_match_evaluation2"

f1 = open(input_file, "r")
found_topos = set()
sttl_reg_set = sttl.get_sttl_with_reg(hier_file)
found_file = pan.read_csv(f1, delimiter='\t', names=["Geo Title", "Cornu Title", "Cornu Title Other",
            "lat", "lon", "Cornu Region", "Geo Prov","Cornu URI", "Status", "Match Method"])
cornu_topos_matched = set()
eval_list = []
for index, row in found_file.iterrows():
    print(row)
    if row["Status"] == "exact":
        tmp = row["Geo Title"] + "-" + row["Geo Prov"]
        if tmp in found_topos:
            eval_list.append(row)
        else:
            found_topos.add(row["Geo Title"] + "-" + row["Geo Prov"])
        if row["Cornu URI"] in cornu_topos_matched:
            eval_list.append(row)
        else:
            cornu_topos_matched.add(row["Cornu URI"])
with open(exact_evaluation, 'w', encoding="utf8") as eval_file:
        writer = csv.writer(eval_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for el in eval_list:
            writer.writerow(el)
# not_found_topos = [item for item in sttl_reg_set if item not in found_topos]
# print(len(found_topos))
# print(len(not_found_topos))
# gm.get_cornu_matches(not_found_topos, hier_file, cornu_places, input_file, mf.jaro_match,
#                      "NA", "Jaro distance 0.85", cornu_topos_matched)
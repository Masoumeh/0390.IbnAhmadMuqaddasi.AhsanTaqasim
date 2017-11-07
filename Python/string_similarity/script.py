import get_sttl_reg as sttl
import get_matches as gm
import match_functions as mf
from graph import create_graph as cg

found_set = set()
sttl_reg_set = set()
cornu_places = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/places.geojson"
hier_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_hier_all"
routes_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_triples_route_wReg"
matches_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/string_similarity/match_results_exact_noReg_routes"
# jaro_dist_matches_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/string_similarity/levenstein_match"
sttl_reg_set = sttl.get_sttl_with_reg(hier_file)
# sttl_reg_set = cg.create_graph_csv(routes_file)

g_cornu = cg.create_graph_geojson("../../Data/routes.json", "../../Data/places_new_structure.geojson")
print(len(sttl_reg_set.nodes()))
# for n in sttl_reg_set.nodes():
#     sttl_reg_set.add(n + "/null")
# print(sttl_reg_set)
cornu_topos_matched = set()
print(type(sttl_reg_set))
found_set = gm.get_cornu_matches(sttl_reg_set, cornu_places,
                                 #g_cornu,
                                 matches_file,
                                 mf.exact_noReg_match, "exact", "exact - noReg", cornu_topos_matched)
# print(len(found_set))
# not_found = [item for item in sttl_reg_set if item not in found_set]
# found_set |= gm.get_cornu_matches(not_found, hier_file, cornu_places, jaro_dist_matches_file, mf.jaro_match, "NA")



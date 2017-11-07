from graph import create_graph as cg
import match_functions as mf
import get_matches as gm


found_set = set()
cornu_places = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/places.geojson"
matches_file = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/string_similarity/match_results_routes"

g_txt = cg.create_graph_csv("../../Data/Muqaddasi/muq_triples_route")
g_cornu = cg.create_graph_geojson("../../Data/routes.json", "../../Data/places_new_structure.geojson")

txt_nodes = g_txt.nodes()
print(len(g_txt.nodes()))

# cornu_topos_matched = set()
# found_set = gm.get_cornu_route_matches(g_txt, cornu_places, g_cornu, matches_file,
#                                  mf.exact_node_match, "exact", "exact", cornu_topos_matched)
# print(found_set)

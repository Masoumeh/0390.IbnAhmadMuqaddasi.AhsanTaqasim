import json
import geograph.simplify_cornu_routes as scr
import geograph.simplify_muq_routes as smr

import geograph.simplify_cornu_postprocessing as postp_c
import geograph.simplify_muq_postprocessing as postp_m
import geojson

f1 = open("../../Data/routes.json", 'r')
json_routes = json.load(f1)
# f1_muq = open("../../Data/tripleRoutes_with_meter_basic_values", 'r')
# json_routes = json.load(f1_muq)

f2 = open("../../Data/places.geojson", 'r')
json_uris = json.load(f2)

json_found = scr.simplify_cornu_routes(json_uris, json_routes)
# json_found = smr.simplify_muq_routes(json_uris, json_routes)

tmp_features = postp_c.postprocess_simplified_network(json_routes, json_uris, json_found)
# tmp_features = postp_m.postprocess_simplified_network(json_routes, json_uris, json_found)
with open("../../Data/new_simplified_cornu_coords_postProcessed_loop2.geojson", 'w') as outfile:
    geojson.dump(tmp_features, outfile, indent=4, ensure_ascii=False)

# with open("../../Data/new_simplified_muq_coords_post.geojson", 'w') as outfile:
#     geojson.dump(tmp_features, outfile, indent=4, ensure_ascii=False)
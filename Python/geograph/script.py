import json
import geograph.simplify_cornu_routes as scr
import geograph.simplify_cornu_postprocessing as postp
import geojson

f1 = open("../../Data/routes.json", 'r')
json_routes = json.load(f1)

f2 = open("../../Data/places.geojson", 'r')
json_uris = json.load(f2)

json_found = scr.simplify_cornu_routes(json_uris, json_routes)
print("json_found")

tmp_features = postp.postprocess_simplified_network(json_routes, json_uris, json_found)

with open("../../Data/new_simplified_cornu_coords_postProcessed_loop.geojson", 'w') as outfile:
    geojson.dump(tmp_features, outfile, indent=4, ensure_ascii=False)
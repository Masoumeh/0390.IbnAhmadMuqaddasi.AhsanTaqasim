import json, csv
import net_simplification.simplify_cornu_routes as scr
import net_simplification.simplify_muq_routes as smr

import net_simplification.simplify_cornu_postprocessing as postp_c
import net_simplification.simplify_muq_postprocessing as postp_m
import geojson

# f1 = open("../../Data/routes.json", 'r')
# json_routes = json.load(f1)
f1_muq = open("../../Data/tripleRoutes_with_meter_basic_values", 'r')
json_routes = json.load(f1_muq)

f2 = open("../../Data/places.geojson", 'r')
json_uris = json.load(f2)

# json_found = scr.simplify_cornu_routes(json_uris, json_routes)
json_found = smr.simplify_muq_routes(json_uris, json_routes)

# tmp_features = postp_c.postprocess_simplified_network(json_routes, json_uris, json_found[0], json_found[1])
tmp_features = postp_m.postprocess_simplified_network(json_routes, json_uris, json_found[0], json_found[1])
# with open("../../Data/new_simplified_cornu_coords_postProcessed_loop2.geojson", 'w') as outfile:
#     geojson.dump(tmp_features[0], outfile, indent=4, ensure_ascii=False)
#
# with open("../../Data/new_simplified_cornu_coords_postProcessed_loop2_SElines.geojson", 'w') as outfile:
#     geojson.dump(tmp_features[1], outfile, indent=4, ensure_ascii=False)

with open("../../Data/new_simplified_muq_coords_post.geojson", 'w') as outfile:
    geojson.dump(tmp_features[0], outfile, indent=4, ensure_ascii=False)

with open("../../Data/new_simplified_muq_coords_post_lines.geojson", 'w') as outfile:
    geojson.dump(tmp_features[1], outfile, indent=4, ensure_ascii=False)
    with open("../../Data/new_simplified_muq_coords_post_edges.csv", 'w') as edgeFile:
        writer = csv.writer(edgeFile, delimiter=',')
        for l in geojson.loads(geojson.dumps(tmp_features[1]['features'])):
            writer.writerow([l['properties']['start'], l['geometry']['coordinates'][0],
                            l['properties']['end'], l['geometry']['coordinates'][-1]])


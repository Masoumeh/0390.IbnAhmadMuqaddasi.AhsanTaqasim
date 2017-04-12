import geojson
import networkx as nx
import geograph.graph as ggraph
import geograph.map  as ggeo

def postprocess_simplified_network(json_routes, json_uris, json_found_json):
    tmp_features = json_found_json
    G = ggraph.createGraphFromJSON(json_routes)
    simplifed_URIs = []
    not_found_uris = []
    new_coords = {}
    for d in json_found_json['features']:
        simplifed_URIs.append(d['properties']['URI'])
    for node in G.nodes():
        if "ROUTPOINT" not in node and "ROUTEPOINT" not in node:
            if node not in simplifed_URIs:
                not_found_uris.append(node)
    while len(not_found_uris) > 0:
        for uri in not_found_uris:
            nei = ggraph.iterative_bfs(G, uri, 2)
            nei_degree = []
            curr_uri_data = ggraph.find_coords_of_uri(uri, json_uris)
            curr_uri_coords = curr_uri_data[0]
            curr_uri_reg = curr_uri_data[1]
            for n in nei:
                shortest_dist = nx.shortest_path_length(G, uri, n, 'length')
                nei_degree.append((n, shortest_dist))
            sorted(nei_degree, key=lambda x: x[1])
            if (len(nei_degree) >= 2):
                start = nei_degree[0][0]
                end = nei_degree[1][0]
                startData = ggraph.find_coords_of_uri(start, json_uris)
                if startData == None and start in new_coords:
                    startData = new_coords[start]
                if startData == None:
                    startData = ggraph.find_coords_of_uri(start, json_uris)

                startCoord = startData[0]
                startReg = startData[1]
                endData = ggraph.find_coords_of_uri(end, json_uris)
                if endData == None and end in new_coords:
                    endData = new_coords[end]

                if endData == None:
                    endData = ggraph.find_coords_of_uri(end, json_uris)
                endCoord = endData[0]
                endReg = endData[1]
                distances = {}
                idx = None
                paths = []
                p = nx.all_shortest_paths(G, uri, start, weight='length')
                paths.append(list(p))
                ggraph.find_path_distance(distances, idx, paths[0],json_routes)
                sum_dist1 = 0
                for dist in distances:
                    sum_dist1 += distances[dist]
                distances = {}
                paths = []
                p = nx.all_shortest_paths(G, uri, end, weight='length')
                paths.append(list(p))
                idx = None
                ggraph.find_path_distance(distances, idx, paths[0],json_routes)
                sum_dist2 = 0
                for dist in distances:
                    sum_dist2 += distances[dist]
                start_end_distance = ggeo.get_path_length(startCoord[0], startCoord[1], endCoord[0], endCoord[1])
                sum_dist = sum_dist1 + sum_dist2
                prop_d = (float(sum_dist1) * float(start_end_distance)) / float(sum_dist)

                start_end_bearing = ggeo.calculate_initial_compass_bearing(startCoord, endCoord)
                lat_lon = ggeo.find_intermediate_coord(prop_d, start_end_bearing, startCoord[0], endCoord[1])
                tmp_features['features'].append(geojson.Feature(geometry=geojson.Point((lat_lon[1], lat_lon[0])),
                                                                properties={'URI': uri, 'status': 'new2',
                                                                            'region': curr_uri_reg}))
                new_coords[uri] = [lat_lon, curr_uri_reg]
                not_found_uris.remove(uri)
    return tmp_features
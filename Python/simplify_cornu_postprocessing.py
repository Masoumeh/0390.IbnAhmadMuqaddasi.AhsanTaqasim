import json
import geopy
import geopy.distance
import networkx as nx
import math
import geojson
import collections
import createGraphFromJSON as cg
import simplify_cornu_routes as scr

def find_coords_of_uri(uri, fileName):
    coords = []
    with open(fileName) as routesFile:
        allData = json.load(routesFile)
        for d in allData['features']:
            if d['properties']['URI'] == uri:
                return [(
                    float(d['geometry']['coordinates'][1]), float(d['geometry']['coordinates'][0])),
                d['properties']['region']]
def postprocess_simplified_network(routesFile, simplified_networkfile):
    G = cg.createGraphFromJSON(routesFile)
    print(G.number_of_nodes())
    print(G.number_of_edges())

    print(nx.number_connected_components(G))
    simplifed_URIs = []
    not_found_uris = []
    new_coords = {}
    with open(simplified_networkfile) as snf:
        data = json.load(snf)
        tmp_features = data
        for d in data['features']:
            simplifed_URIs.append(d['properties']['URI'])
        print(len(simplifed_URIs))
        for node in G.nodes():
            if "ROUTPOINT" not in node and "ROUTEPOINT" not in node:
                print("node: ", node)
                if node not in simplifed_URIs:
                    not_found_uris.append(node)
        print(not_found_uris)
        while len(not_found_uris) > 0:
            print(len(not_found_uris))
            for uri in not_found_uris:
                nei = scr.iterative_bfs(G, uri, 2)
                nei_degree = []
                curr_uri_data = scr.find_coords_of_uri(uri, "../Data/places.geojson")
                curr_uri_coords = curr_uri_data[0]
                curr_uri_reg = curr_uri_data[1]
                for n in nei:
                    # ndata = find_coords_of_uri(n, "../Data/simplified_cornu_coords_uricoords.geojson")
                    # if ndata == None:
                    #     print("if: ", n)
                    #     ndata = scr.find_coords_of_uri(n, "../Data/places.geojson")
                    # if ndata == None:
                    #     print("none: ", n)
                    #     ndata = scr.find_coords_of_uri(n, "../Data/places.geojson")
                    # ncoord = ndata[0]
                    # dist = scr.getPathLength(curr_uri_coords[0], curr_uri_coords[1], ncoord[0], ncoord[1])
                    # nei_degree.append((n, dist))
                    shortest_dist = nx.shortest_path_length(G, uri, n, 'length')
                    nei_degree.append((n, shortest_dist))
                sorted(nei_degree, key=lambda x: x[1])
                if (len(nei_degree) >= 2):
                    start = nei_degree[0][0]
                    end = nei_degree[1][0]
                    startData = find_coords_of_uri(start, "../Data/simplified_cornu_coords_uricoords.geojson")
                    if startData == None and start in new_coords:
                        startData = new_coords[start]
                    if startData == None:
                        startData = scr.find_coords_of_uri(start, "../Data/places.geojson")

                    startCoord = startData[0]
                    startReg = startData[1]
                    endData = find_coords_of_uri(end, "../Data/simplified_cornu_coords_uricoords.geojson")
                    if endData == None and end in new_coords:
                        endData = new_coords[end]

                    if endData == None:
                        endData = scr.find_coords_of_uri(end, "../Data/places.geojson")
                    endCoord = endData[0]
                    endReg = endData[1]
                    distances = {}
                    idx = None
                    paths = []
                    p = nx.all_shortest_paths(G, uri, start, weight='length')
                    paths.append(list(p))
                    scr.find_path_distance(distances, idx, paths[0])
                    sum_dist1 = 0
                    for dist in distances:
                        sum_dist1 += distances[dist]
                    distances = {}
                    paths = []
                    p = nx.all_shortest_paths(G, uri, end, weight='length')
                    paths.append(list(p))
                    idx = None
                    scr.find_path_distance(distances, idx, paths[0])
                    sum_dist2 = 0
                    for dist in distances:
                        sum_dist2 += distances[dist]
                    start_end_distance = scr.getPathLength(startCoord[0], startCoord[1], endCoord[0], endCoord[1])
                    sum_dist = sum_dist1+sum_dist2
                    prop_d = (float(sum_dist1) * float(start_end_distance)) / float(sum_dist)

                    start_end_bearing = scr.calculate_initial_compass_bearing(startCoord, endCoord)
                    lat_lon = scr.find_intermediate_coord(prop_d, start_end_bearing, startCoord[0], endCoord[1])
                    tmp_features['features'].append(geojson.Feature(geometry=geojson.Point((lat_lon[1], lat_lon[0])),
                                                             properties= {'URI': uri, 'status': 'new2',
                                                                          'region' : curr_uri_reg}))
                    new_coords[uri] = [lat_lon, curr_uri_reg]
                    not_found_uris.remove(uri)
            with open("../Data/simplified_cornu_coords_postProcessed_loop.geojson", 'w') as outfile:
                geojson.dump(tmp_features, outfile, indent=4, ensure_ascii=False)


postprocess_simplified_network("../Data/routes.json", "../Data/simplified_cornu_coords_uricoords_orig.geojson")

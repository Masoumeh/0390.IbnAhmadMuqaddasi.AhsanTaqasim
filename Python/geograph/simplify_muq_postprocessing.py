import geojson
import networkx as nx
import geograph.graph as ggraph
import geograph.map  as ggeo
import createGraphFromJSON_geoText_toJSON as cgjt


def postprocess_simplified_network(json_routes, json_uris, json_found_json):
    tmp_features = json_found_json
    # print("len1: ", len(tmp_features))
    # G = ggraph.createGraphFromJSON(json_routes)
    G = cgjt.create_graph(json_routes)
    simplifed_URIs = {}
    not_found_uris = []
    final_not_found = []
    new_coords = {}
    for d in json_found_json['features']:
        simplifed_URIs[d['properties']['URI']] = [(d['geometry']['coordinates'][1],d['geometry']['coordinates'][0]),
                                                  d['properties']['region']]

    for node in G.nodes():
        # if "ROUTPOINT" not in node and "ROUTEPOINT" not in node:
            if node not in simplifed_URIs:
                not_found_uris.append(node)
    print("first nf: ", len(not_found_uris))
    final_not_found = []
    # while len(not_found_uris) > 0:
    prev_not_found_len = len(not_found_uris)
    while prev_not_found_len > len(final_not_found):
        final_not_found = not_found_uris
        prev_not_found_len = len(final_not_found)
        print('prev: ', prev_not_found_len, " len final: ", len(final_not_found))
        for uri in not_found_uris:
            # print("uri: ", uri)
            # nei = ggraph.iterative_bfs(G, uri, 2)
            nei = ggraph.bfs_for_postprocess(G, uri, 2, simplifed_URIs, new_coords, json_uris)
            # return
            nei_degree = []
            startData = []
            endData = []
            curr_uri_data = ggraph.find_coords_of_uri(uri, json_uris)
            if curr_uri_data != "NA":
                curr_uri_reg = curr_uri_data[1]
            else:
                curr_uri_reg = "undefined"
            for n in nei:
                shortest_dist = nx.shortest_path_length(G, uri, n, 'length')
                nei_degree.append((n, shortest_dist))
            sorted(nei_degree, key=lambda x: x[1])
            # print("nei: ", nei_degree)
            # if (len(nei_degree) >= 2):
            nei_with_coords = {}
            nei_with_coords_list = []
            for i in range(len(nei_degree)):
                if len(nei_with_coords) >= 2:
                    break
                if nei_degree[i][0] in simplifed_URIs:
                    nei_with_coords[nei_degree[i][0]] = simplifed_URIs[nei_degree[i][0]]
                    # print("s in sim: ", startData)
                elif nei_degree[i][0] in new_coords:
                    nei_with_coords[nei_degree[i][0]] = new_coords[nei_degree[i][0]]
                    # print("s in new: ", startData)
                else:
                    nei_with_coords[nei_degree[i][0]] = ggraph.find_coords_of_uri(nei_degree[i][0], json_uris)
                if nei_with_coords[nei_degree[i][0]] not in ["NA", None]:
                    nei_with_coords_list.append(nei_degree[i][0])
            if (len(nei_with_coords_list) >= 2):
                # print("nei_with_coords_list: ", nei_with_coords_list)
                start = nei_with_coords_list[0]
                startData = nei_with_coords[nei_with_coords_list[0]]
                end = nei_with_coords_list[1]
                endData = nei_with_coords[nei_with_coords_list[1]]

                # if start in simplifed_URIs:
                #     startData = simplifed_URIs[start]
                #     # print("s in sim: ", startData)
                # elif start in new_coords:
                #     startData = new_coords[start]
                #     # print("s in new: ", startData)
                # else:
                #     startData = ggraph.find_coords_of_uri(start, json_uris)
                    # print("s in places: ", startData)
                # if startData == None and start in new_coords:
                #     startData = new_coords[start]
                # if startData == None:
                #     startData = ggraph.find_coords_of_uri(start, json_uris)

                # if end in simplifed_URIs:
                #     endData = simplifed_URIs[end]
                #     # print("e in sim: ", endData)
                #
                # elif end in new_coords:
                #     endData = new_coords[end]
                #     # print("e in new: ", endData)
                # else:
                #     endData = ggraph.find_coords_of_uri(end, json_uris)

                # if endData == None and end in new_coords:
                #     endData = new_coords[end]
                #
                # if endData == None:
                #     endData = ggraph.find_coords_of_uri(end, json_uris)
                # if all(x not in ["NA", None] for x in [startData, endData]):
                startCoord = startData[0]
                startReg = startData[1]
                endCoord = endData[0]
                endReg = endData[1]
                # print("start: ", start, " scoords: ", startCoord, " sreg: ", startReg)
                # print("end: ", end, " ecoords: ", endCoord, " ereg: ", endReg)

                distances = {}
                idx = None
                paths = []
                p = nx.all_shortest_paths(G, uri, start, weight='length')
                paths.append(list(p))
                # paths = list(p)
                ggraph.find_path_distance(distances, idx, paths[0][0], json_routes)
                # ggraph.find_path_distance(distances, idx, list(p), json_routes)
                # print("s distances: ", distances)

                sum_dist1 = 0
                for dist in distances:
                    sum_dist1 += distances[dist]
                distances = {}
                paths = []
                p = nx.all_shortest_paths(G, uri, end, weight='length')
                paths.append(list(p))
                # paths = list(p)
                # print("paths 2: ", p)

                idx = None
                ggraph.find_path_distance(distances, idx, paths[0][0], json_routes)
                # print("e distances: ", distances)

                # ggraph.find_path_distance(distances, idx, list(p), json_routes)
                sum_dist2 = 0

                for dist in distances:
                    sum_dist2 += distances[dist]
                start_end_distance = ggeo.get_path_length(startCoord[0], startCoord[1], endCoord[0], endCoord[1])
                sum_dist = sum_dist1 + sum_dist2
                # print("dist1: ", sum_dist1, " sdist2: ", sum_dist2)
                # print("dir distance: ", start_end_distance)
                prop_d = (float(sum_dist1) * float(start_end_distance)) / float(sum_dist)
                # print("prop d: ", prop_d)

                start_end_bearing = ggeo.calculate_initial_compass_bearing(startCoord, endCoord)
                # print("bearing " , start_end_bearing)
                lat_lon = ggeo.find_intermediate_coord(prop_d, start_end_bearing, startCoord[0], startCoord[1])
                tmp_features['features'].append(geojson.Feature(geometry=geojson.Point((lat_lon[1], lat_lon[0])),
                                                                properties={'URI': uri, 'status': 'new2',
                                                                            'region': curr_uri_reg}))
                new_coords[uri] = [lat_lon, curr_uri_reg]
                # print("uri new coords: ", lat_lon)
                # print(geojson.Feature(geometry=geojson.Point((lat_lon[0], lat_lon[1])),
                #                                                 properties={'URI': uri, 'status': 'new2',
                #                                                             'region': curr_uri_reg}))
                final_not_found.remove(uri)
            # if no neighbour with degree >2 and coordinates are found,
            # go for any other neighbors (even with degree <= 2 which have coordinate)
            else:
                nei_with_coords = {}
                nei_with_coords_list = []
                neighbours = G.neighbors(uri)
                for nei in neighbours:
                    if len(nei_with_coords) >= 2:
                        break
                    if nei in simplifed_URIs:
                        nei_with_coords[nei] = simplifed_URIs[nei]
                        # print("s in sim: ", startData)
                    elif nei in new_coords:
                        nei_with_coords[nei] = new_coords[nei]
                        # print("s in new: ", startData)
                    else:
                        nei_with_coords[nei] = ggraph.find_coords_of_uri(nei, json_uris)
                    if nei_with_coords[nei] not in ["NA", None]:
                        nei_with_coords_list.append(nei)
                if (len(nei_with_coords_list) >= 2):
                    # print("dir nei_with_coords_list: ", nei_with_coords_list)
                    start = nei_with_coords_list[0]
                    startData = nei_with_coords[nei_with_coords_list[0]]
                    end = nei_with_coords_list[1]
                    endData = nei_with_coords[nei_with_coords_list[1]]
                    startCoord = startData[0]
                    startReg = startData[1]
                    endCoord = endData[0]
                    endReg = endData[1]
                    sum_dist1 = G[uri][start]['length']
                    sum_dist2 = G[uri][end]['length']
                    start_end_distance = ggeo.get_path_length(startCoord[0], startCoord[1], endCoord[0], endCoord[1])
                    sum_dist = sum_dist1 + sum_dist2
                    start_end_bearing = ggeo.calculate_initial_compass_bearing(startCoord, endCoord)
                    prop_d = (float(sum_dist1) * float(start_end_distance)) / float(sum_dist)
                    lat_lon = ggeo.find_intermediate_coord(prop_d, start_end_bearing, startCoord[0], startCoord[1])
                    tmp_features['features'].append(geojson.Feature(geometry=geojson.Point((lat_lon[1], lat_lon[0])),
                                                                    properties={'URI': uri, 'status': 'new3',
                                                                                'region': "not_set"}))
                    new_coords[uri] = [lat_lon, curr_uri_reg]
                    final_not_found.remove(uri)

                else:
                    not_found_uris = final_not_found
            # if uri in not_found_uris:
            #     not_found_uris.remove(uri)
            # else:
            #     print("not in not found: ", uri)
    print("final nF: ", len(final_not_found))
    for n in final_not_found:
        print("node: ", n, " deg: ", G.degree(n))
        for nei in G.neighbors(n):
            if nei not in [simplifed_URIs, new_coords] and ggraph.find_coords_of_uri(nei, json_uris) == "NA":
                print("null neighbors: ", nei)
            else:
                print("not null: ", nei)
    return tmp_features
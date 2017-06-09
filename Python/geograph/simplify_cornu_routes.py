import geojson
import networkx as nx
import geograph.graph as ggraph
import geograph.map  as ggeo


def simplify_cornu_routes(json_uris, json_routes):
    G = ggraph.createGraphFromJSON(json_routes)
    higher_degree_nodes = []
    degree = 3
    node_neighbours = {}
    # paths = {}
    pFeatures = []
    lFeatures = []
    processed_nodes = set()
    cnt = 0
    for node in G.nodes():
        if "ROUTPOINT" not in node and "ROUTEPOINT" not in node:
            cnt = cnt +1
            if G.degree(node) >= degree:
                higher_degree_nodes.append(node)
                node_neighbours[node] = ggraph.iterative_bfs(G, node, degree)
                # processed_nodes.update(node_neighbours[node])
    print("nodes : ", cnt)
    uri_coord = {}
    in_coords = set()
    # for n in processed_nodes:
    for n in higher_degree_nodes:
        nData = ggraph.find_coords_of_uri(n, json_uris)
        nCoords = nData[0]
        nReg = nData[1]
        if n not in uri_coord:
            uri_coord[n] = [nCoords[0], nCoords[1]]
            n_feature = geojson.Feature(geometry=geojson.Point((nCoords[1], nCoords[0])),
                                    properties={'URI': n, "region": nReg})
            pFeatures.append(n_feature)
        for ne in node_neighbours[n]:
            if ne not in uri_coord:
                neData = ggraph.find_coords_of_uri(ne, json_uris)
                neCoords = neData[0]
                neReg = neData[1]
                uri_coord[ne] = [neCoords[0], neCoords[1]]
                ne_feature = geojson.Feature(geometry=geojson.Point((neCoords[1], neCoords[0])),
                                             properties={'URI': ne, "region": neReg})
                pFeatures.append(ne_feature)

    cnt = 0
    for node in higher_degree_nodes:
        cnt = cnt + 1
        paths = []
        for nei in node_neighbours[node]:
            p = nx.all_shortest_paths(G, source=node, target=nei, weight='length')
            paths.append(list(p))

        for path in paths:
            # if len(path) > 1:
            #     print("len path: ", len(path), " - ", path)
            for p in path:
                distances = {}
                idx = None
                startData = ggraph.find_coords_of_uri(p[0], json_uris)
                start = startData[0]
                startReg = startData[1]
                endData = ggraph.find_coords_of_uri(p[-1], json_uris)
                end = endData[0]
                endReg = endData[1]
                start_end_bearing = ggeo.calculate_initial_compass_bearing(start, end)
                # start_end_distance = geopy.distance.vincenty(start, end).miles
                start_end_distance = ggeo.get_path_length(start[0], start[1], end[0], end[1])
                ggraph.find_path_distance(distances, idx, p, json_routes)
                sum_dist = 0
                for dist in distances:
                    sum_dist += distances[dist]
                for i in range(len(p) - 1):
                    topo_to_coordinate = ""
                    if "ROUTPOINT" not in p[i] and p[i + 1] not in uri_coord:
                        if "ROUTPOINT" not in p[i + 1]:
                            topo_to_coordinate = p[i + 1]
                            # print("if: ", topo_to_coordinate)
                            d = next(v for k, v in distances.items() if all(x in k for x in [p[i], p[i + 1]]))
                        else:
                            topo_to_coordinate = next(s for s in p[i + 1:] if "ROUTPOINT" not in s)
                            # print("else: ", topo_to_coordinate)
                            d = next(
                                v for k, v in distances.items() if all(x in k for x in [p[i], topo_to_coordinate]))
                        if topo_to_coordinate in uri_coord:
                            in_coords.add(topo_to_coordinate)
                        prop_d = (float(d) * float(start_end_distance)) / float(sum_dist)
                        if path[0][i] in uri_coord:
                            point = uri_coord[p[i]]
                        else:
                            point = uri_coord[p[i - 1]]

                        lat_lon = ggeo.find_intermediate_coord(prop_d, start_end_bearing, point[0], point[1])
                        if topo_to_coordinate not in uri_coord:
                            uri_coord[topo_to_coordinate] = [lat_lon[0], lat_lon[1]]
                            properties = {'URI': topo_to_coordinate, 'status': 'new',
                                          'region': ggraph.find_coords_of_uri(topo_to_coordinate, json_uris)[1]}
                            tmp_pFeature = geojson.Feature(geometry=geojson.Point((lat_lon[1], lat_lon[0])),
                                                           properties=properties)
                            pFeatures.append(tmp_pFeature)
                            # lFeatures.append(tmp_lFeature)
                            geojson.FeatureCollection(pFeatures)
                            # geojson.FeatureCollection(lFeatures)

    pf = geojson.FeatureCollection(pFeatures)
    return pf


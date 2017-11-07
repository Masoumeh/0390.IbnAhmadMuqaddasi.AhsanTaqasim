import geojson
import networkx as nx
import net_simplification.graph as ggraph
import net_simplification.map  as ggeo
import createGraphFromJSON_geoText_toJSON as cgjt

def simplify_muq_routes(json_uris, json_routes):
    G = cgjt.create_graph(json_routes)
    print("g nodes: ", G.number_of_nodes())
    higher_degree_nodes = []
    degree = 3
    node_neighbours = {}
    # paths = {}
    pFeatures = []
    lFeatures = []
    processed_nodes = set()
    for node in G.nodes():
        # if "ROUTPOINT" not in node and "ROUTEPOINT" not in node:
            if G.degree(node) >= degree:
                higher_degree_nodes.append(node)
                node_neighbours[node] = ggraph.iterative_bfs(G, node, degree)
                # processed_nodes.update(node)
                # processed_nodes.update(node_neighbours[node])
    # print("processed: ", len(processed_nodes), " ", processed_nodes)
    # print("high deg: len: ", len(higher_degree_nodes), " ", higher_degree_nodes)
    uri_coord = {}
    in_coords = set()
    # for n in processed_nodes:
    for n in higher_degree_nodes:
        nData = ggraph.find_coords_of_uri(n, json_uris)
        if nData != "NA":
            nCoords = nData[0]
            nReg = nData[1]
            uri_coord[n] = [nCoords[0], nCoords[1]]
            n_feature = geojson.Feature(geometry=geojson.Point((nCoords[1], nCoords[0])),
                                        properties={'URI': n, "region": nReg})
            pFeatures.append(n_feature)
            for ne in node_neighbours[n]:
                if ne not in uri_coord:
                    neData = ggraph.find_coords_of_uri(ne, json_uris)
                if neData != "NA":
                    neCoords = neData[0]
                    neReg = neData[1]
                    uri_coord[ne] = [neCoords[0], neCoords[1]]
                    ne_feature = geojson.Feature(geometry=geojson.Point((neCoords[1], neCoords[0])),
                                                properties={'URI': ne, "region": neReg})
                    pFeatures.append(ne_feature)
        # else:
        #     print("higher deg wo cornuURI: ", n)
    # print("fist new coords: ", uri_coord)
    cnt = 0
    degree_one_no_uri = set()
    for node in higher_degree_nodes:
    #     if ggraph.find_coords_of_uri(node, json_uris) == "NA":
    #         print(node)
    #     for n in node_neighbours[node]:
    #         if ggraph.find_coords_of_uri(n, json_uris) == "NA" and G.degree(n) == 1:
    #             degree_one_no_uri.add(n)
    # print( " nei: ", len(degree_one_no_uri), "  ----  ",degree_one_no_uri)
        if ggraph.find_coords_of_uri(node, json_uris) != "NA":
            # print("node: ", node)
            cnt = cnt + 1
            paths = []
            for nei in node_neighbours[node]:
                p = nx.all_shortest_paths(G, source=node, target=nei, weight='length')
                paths.append(list(p))
            for path in paths:
                distances = {}
                for p in path:
                    # print("len: ",len(path), " p: ", p)
                    idx = None
                    startData = ggraph.find_coords_of_uri(p[0], json_uris)
                    if startData != "NA":
                        start = startData[0]
                        startReg = startData[1]
                    else:
                        continue
                    endData = ggraph.find_coords_of_uri(p[-1], json_uris)
                    if endData != "NA":
                        end = endData[0]
                        endReg = endData[1]
                    else:
                        continue
                    se_lfeature = geojson.Feature(geometry=geojson.LineString([(start[1], start[0]), (end[1], end[0])]),
                                                  properties={'start': p[0], 'end': p[-1]})
                    lFeatures.append(se_lfeature)
                    start_end_bearing = ggeo.calculate_initial_compass_bearing(start, end)
                    # start_end_distance = geopy.distance.vincenty(start, end).miles
                    start_end_distance = ggeo.get_path_length(start[0], start[1], end[0], end[1])
                    distances = ggraph.find_path_distance(idx, p, json_routes)
                    # print("distances: ", distances)
                    sum_dist = 0
                    for dist in distances:
                        sum_dist += distances[dist]

                    for i in range(len(p) - 1):
                        # print("i: ", i)
                        topo_to_coordinate = ""
                        if p[i + 1] not in uri_coord:
                            topo_to_coordinate = p[i + 1]
                            # print("topo: ", topo_to_coordinate,  "pi, pi+1: ", p[i], " ", p[i+1] )
                            for k,v in distances.items():
                                if all(x in k for x in [p[i], p[i + 1]]):
                                    d = v
                                    break
                            # d = next(v for k, v in distances.items() if all(x in k for x in [p[i], p[i + 1]]))
                            # TODO: should remove this line??
                            if topo_to_coordinate in uri_coord:
                                in_coords.add(topo_to_coordinate)
                            prop_d = (float(d) * float(start_end_distance)) / float(sum_dist)
                            if p[i] in uri_coord:
                                point = uri_coord[p[i]]
                                s = p[i]
                            else:
                                # TODO: why??
                                # print("p i wo coords: ", p[i])
                                point = uri_coord[p[i - 1]]

                            lat_lon = ggeo.find_intermediate_coord(prop_d, start_end_bearing, point[0], point[1])
                            if topo_to_coordinate not in uri_coord:
                                # print("new coords: ", topo_to_coordinate, " - ", lat_lon)
                                uri_coord[topo_to_coordinate] = lat_lon#[lat_lon[0], lat_lon[1]]
                                properties = {'URI': topo_to_coordinate, 'status': 'new',
                                              'region': ggraph.find_coords_of_uri(topo_to_coordinate, json_uris)[1]
                                              if ggraph.find_coords_of_uri(topo_to_coordinate, json_uris) != 'NA' else "undefined"}
                                tmp_pFeature = geojson.Feature(geometry=geojson.Point((lat_lon[1], lat_lon[0])),
                                                               properties=properties)
                                tmp_lFeature = geojson.Feature(geometry=geojson.LineString([(point[1], point[0]),
                                                                                            (lat_lon[1], lat_lon[0])]),
                                                               properties={'start': point, "end": topo_to_coordinate})

                                pFeatures.append(tmp_pFeature)
                                lFeatures.append(tmp_lFeature)
                                # geojson.FeatureCollection(pFeatures)
                                # print("feature: ", tmp_pFeature)
                            # geojson.FeatureCollection(lFeatures)

    pf = geojson.FeatureCollection(pFeatures)
    lf = geojson.FeatureCollection(lFeatures)
    # with open("../../Data/new_simplified_muq_coords.geojson", 'w') as outfile:
    #     geojson.dump(pf, outfile, indent=4, ensure_ascii=False)
    return [pf, lf]

# simplify_muq_routes("../../Data/places.geojson", "../../Data/tripleRoutes_with_basic_values")

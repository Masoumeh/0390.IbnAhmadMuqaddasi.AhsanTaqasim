import json
import geopy
import geopy.distance
import networkx as nx
import math
import geojson
import collections
import createGraphFromJSON as cg


def iterative_bfs(graph, start, deg):
    bfs_res = nx.bfs_edges(graph, start)
    bfs_pre = nx.bfs_predecessors(graph, start)
    # print(list(bfs_pre))
    found_so_far = []
    found = 0
    start_nexts = {}
    # print(graph.degree("SUWA_378E337N_S"))
    neigh = graph.neighbors(start)
    neigh_proccessed = set()

    for key in bfs_res:
        if len(found_so_far) > graph.degree(start):
        # if all(item in neigh for item in neigh_proccessed) and len(neigh_proccessed) == len(neigh):
            return found_so_far
        # if "ROUTPOINT" in key[0]:
        #     continue
        if graph.degree(key[1]) == 1 and key[1] not in found_so_far:
            found_so_far.append(key[1])

        if (key[0] != start and graph.degree(key[0]) < deg) or "ROUTPOINT" in key[0]:
            continue
        val = key[0]
        is_parent_with_high_deg = False
        while val != start:
            # print(val, bfs_pre[val], graph.degree(bfs_pre[val]))
            # if val in neigh:
            #     neigh_proccessed.add(val)
            if bfs_pre[val] != start and graph.degree(bfs_pre[val]) >= deg and "ROUTPOINT" not in bfs_pre[val]:
                is_parent_with_high_deg = True
                break
            val = bfs_pre[val]
            # print("val: ",val)

        if is_parent_with_high_deg:
            continue
        if key[0] != start and graph.degree(key[0]) >= deg and "ROUTPOINT" not in key[0] and not is_parent_with_high_deg:
                if key[0] not in found_so_far:
                    found_so_far.append(key[0])
        if key[0] == start and graph.degree(key[1]) >= deg and "ROUTPOINT" not in key[1]:
                if key[1] not in found_so_far:
                    found_so_far.append(key[1])
    return found_so_far


def getPathLength(lat1, lng1, lat2, lng2):
    '''calculates the distance between two lat, long coordinate pairs'''
    R = 6371000  # radius of earth in m
    lat1rads = math.radians(lat1)
    lat2rads = math.radians(lat2)
    deltaLat = math.radians((lat2 - lat1))
    deltaLng = math.radians((lng2 - lng1))
    a = math.sin(deltaLat / 2) * math.sin(deltaLat / 2) + math.cos(lat1rads) * math.cos(lat2rads) * math.sin(
        deltaLng / 2) * math.sin(deltaLng / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d


def getDestinationLatLong(lat, lng, azimuth, distance):
    '''returns the lat an long of destination point
    given the start lat, long, aziuth, and distance'''
    R = 6378.1  # Radius of the Earth in km
    brng = math.radians(azimuth)  # Bearing is degrees converted to radians.
    d = float(distance) / 1000  # Distance m converted to km
    lat1 = math.radians(lat)  # Current dd lat point converted to radians
    lon1 = math.radians(lng)  # Current dd long point converted to radians
    lat2 = math.asin(math.sin(lat1) * math.cos(d / R) + math.cos(lat1) * math.sin(d / R) * math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d / R) * math.cos(lat1),
                             math.cos(d / R) - math.sin(lat1) * math.sin(lat2))
    # convert back to degrees
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return (lat2, lon2)


def calculateBearing(lat1, lng1, lat2, lng2):
    '''calculates the azimuth in degrees from start point to end point'''
    startLat = math.radians(lat1)
    startLong = math.radians(lng1)
    endLat = math.radians(lat2)
    endLong = math.radians(lng2)
    dLong = endLong - startLong
    dPhi = math.log(math.tan(endLat / 2.0 + math.pi / 4.0) / math.tan(startLat / 2.0 + math.pi / 4.0))
    if abs(dLong) > math.pi:
        if dLong > 0.0:
            dLong = -(2.0 * math.pi - dLong)
        else:
            dLong = (2.0 * math.pi + dLong)
    bearing = (math.degrees(math.atan2(dLong, dPhi)) + 360.0) % 360.0
    return bearing


def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.

    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))

    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees

    :Returns:
      The bearing in degrees

    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])
    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                           * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    # return initial_bearing
    return compass_bearing


def find_intermediate_coord(interval, azimuth, lat1, lng1):
    '''returns a coordinate pair inbetween two coordinate
    pairs given the desired interval'''

    # azimuth = calculate_initial_compass_bearing((lat1, lng1), (lat2, lng2))
    return getDestinationLatLong(lat1, lng1, azimuth, float(interval))


def find_distance_of_route(start, end, fileName):
    with open(fileName) as routesFile:
        allData = json.load(routesFile)
        for d in allData['features']:
            if (d['properties']['sToponym'] == start and d['properties']['eToponym'] == end) or (
                            d['properties']['sToponym'] == end and d['properties']['eToponym'] == start):
                return d['properties']['Meter']


def find_coords_of_uri(uri, fileName):
    with open(fileName) as routesFile:
        allData = json.load(routesFile)
        for d in allData['features']:
            if d['properties']['cornuData']['cornu_URI'] == uri:
                return [(
                    float(d['properties']['cornuData']['coord_lat']), float(d['properties']['cornuData']['coord_lon'])),
                d['properties']['cornuData']['region_code']]


def find_node_degree(routesFile ):
    G = cg.createGraphFromJSON(routesFile)
    higher_degree_nodes = []
    degree = 3
    node_neighbours = {}
    # paths = {}
    pFeatures = []
    lFeatures = []
    processed_nodes = set()
    for node in G.nodes():
        if "ROUTPOINT" not in node and "ROUTEPOINT" not in node:
            if G.degree(node) >= degree:
                higher_degree_nodes.append(node)
                # print(node, " ", G.degree(node))
                node_neighbours[node] = iterative_bfs(G, node, degree)
                #print(node," : ",node_neighbours[node])
                processed_nodes.update(node_neighbours[node])
    uri_coord = {}
    in_coords = set()
    for n in processed_nodes:
        nData = find_coords_of_uri(n, "../Data/places.geojson")
        nCoords = nData[0]
        nReg = nData[1]
        uri_coord[n] = [nCoords[0],nCoords[1]]
        n_feature = geojson.Feature(geometry=geojson.Point((nCoords[1], nCoords[0])),
                                        properties={'URI': n, "region": nReg})
        pFeatures.append(n_feature)

    print(len(higher_degree_nodes))
    print(len(processed_nodes))
    # s1 = set(higher_degree_nodes)
    # s2 = set(processed_nodes)
    # print(s2 - s1)
    cnt = 0
    for node in higher_degree_nodes:
        print("node: ", node, " cnt: ", cnt)
        cnt = cnt +1
        paths = []
        for nei in node_neighbours[node]:
            p = nx.all_shortest_paths(G, source=node, target=nei, weight='length')
            paths.append(list(p))
    # paths = nx.all_shortest_paths(G, source=higher_degree_nodes[0], target=node_neighbours[higher_degree_nodes[0]][0], weight='length')
    #     print("paths: ", paths)
        for path in paths:
            distances = {}
            idx = None
            startData = find_coords_of_uri(path[0][0], "../Data/places.geojson")
            start = startData[0]
            startReg = startData[1]
            endData = find_coords_of_uri(path[0][-1], "../Data/places.geojson")
            end = endData[0]
            endReg = endData[1]
            start_end_bearing = calculate_initial_compass_bearing(start, end)
            # start_end_distance = geopy.distance.vincenty(start, end).miles
            start_end_distance = getPathLength(start[0], start[1], end[0], end[1])
            find_path_distance(distances, idx, path)
            # print("distances: ", distances)

            sum_dist = 0
            for dist in distances:
                sum_dist += distances[dist]
            # start_feature = geojson.Feature(geometry=geojson.Point((start[1], start[0])),
            #                                 properties={'URI': path[0][0], "region": startReg})
            # end_feature = geojson.Feature(geometry=geojson.Point((end[1], end[0])),
            #                               properties={'URI': path[0][-1], "region": endReg})
            # start_end_line = geojson.Feature(geometry=geojson.LineString([(start[1], start[0]), (end[1], end[0])]),
            #                                 properties={'s': path[0][0], 'e': path[0][-1]})
            # uri_coord[path[0][0]] = [start[0], start[1]]
            # uri_coord[path[0][-1]] = [end[1], end[0]]
            # if start_feature['properties']['URI'] not in uri_coord:
            #     pFeatures.append(start_feature)
            # # lFeatures.append(start_end_line)
            # if end_feature['properties']['URI'] not in uri_coord:
            #     pFeatures.append(end_feature)
            # print("pfeatures: ", pFeatures)
            # print("uri_coords: ", uri_coord)
            # coords.append(list(start))
            for i in range(len(path[0]) - 3):
                topo_to_coordinate = ""
                if "ROUTPOINT" not in path[0][i] and path[0][i + 1] not in uri_coord:
                    if "ROUTPOINT" not in path[0][i + 1]:
                        topo_to_coordinate = path[0][i + 1]
                        # print("if: ", topo_to_coordinate)
                        d = next(v for k, v in distances.items() if all(x in k for x in [path[0][i], path[0][i + 1]]))
                    else:
                        topo_to_coordinate = next(s for s in path[0][i + 1:] if "ROUTPOINT" not in s)
                        # print("else: ", topo_to_coordinate)
                        d = next(v for k, v in distances.items() if all(x in k for x in [path[0][i], topo_to_coordinate]))
                    if topo_to_coordinate in uri_coord:
                        in_coords.add(topo_to_coordinate)
                    #     continue
                    prop_d = (float(d) * float(start_end_distance)) / float(sum_dist)
                    # d = geopy.distance.VincentyDistance(kilometers = prop_d/1000)
                    if path[0][i] in uri_coord:
                        point = uri_coord[path[0][i]]
                    else:
                        print("pre, i, next: ", path[0][i-1], " ", path[0][i], " ", path[0][i+1])
                        point = uri_coord[path[0][i-1]]

                    # print("topo To: ", topo_to_coordinate)
                    # lat_lon = d.destination(point=point, bearing=start_end_bearing)
                    lat_lon = find_intermediate_coord(prop_d, start_end_bearing, point[0], point[1])
                    if topo_to_coordinate not in uri_coord:
                        uri_coord[topo_to_coordinate] = [lat_lon[0], lat_lon[1]]
                        properties = {'URI': topo_to_coordinate, 'status': 'new',
                                      'region':  find_coords_of_uri(topo_to_coordinate, "../Data/places.geojson")[1]}
                        tmp_pFeature = geojson.Feature(geometry=geojson.Point((lat_lon[1], lat_lon[0])), properties=properties)
                        # tmp_lFeature = geojson.Feature(geometry=geojson.LineString([(uri_coord[path[0][i]][1], uri_coord[path[0][i]][0]),
                        #                                                             (lat_lon[1], lat_lon[0])]),
                        #                                properties={'s': path[0][i], 'e': topo_to_coordinate})
                        pFeatures.append(tmp_pFeature)
                        # lFeatures.append(tmp_lFeature)
                        geojson.FeatureCollection(pFeatures)
                        # geojson.FeatureCollection(lFeatures)
    print("uri cords: ", uri_coord)
    print("in cords: ", in_coords)


    pf = geojson.FeatureCollection(pFeatures)
    # lf = geojson.FeatureCollection(lFeatures)

    # print(pf)
    with open("../Data/simplified_cornu_coords_uricoords.geojson", 'w') as outfile:
        geojson.dump(pf, outfile, indent=4, ensure_ascii=False)
    # with open("../Data/simplified_cornu_lines.geojson", 'w') as outfile:
    #     geojson.dump(lf, outfile, indent=4, ensure_ascii=False)

def find_path_distance(distances, idx, path):
    for i in range(len(path[0]) - 1):
        if idx and i < idx:
            continue
        if "ROUTPOINT" not in path[0][i]:
            tmpStr = (',').join([path[0][i], path[0][i + 1]])
            distances[tmpStr] = find_distance_of_route(path[0][i], path[0][i + 1], "../Data/routes.json")
        if "ROUTPOINT" in path[0][i]:
            # the last toponym in the array, which is not ROUTPOINT, before the current accurance of ROUTPOINT in array
            lastTopo_before_i = [s for s in path[0][:i] if "ROUTPOINT" not in s][-1]
            # get the distance value for the corresponding route section
            lastTopo_dist = next(
                v for k, v in distances.items() if all(x in k for x in [lastTopo_before_i, path[0][i]]))
            currDist = find_distance_of_route(path[0][i], path[0][i + 1], "../Data/routes.json")
            if (',').join([lastTopo_before_i, path[0][i]]) in distances:
                del distances[(',').join([lastTopo_before_i, path[0][i]])]

            # the first toponym in the array, which is not ROUTPOINT, after the current accurance of ROUTPOINT in array
            firstTopo_after_i = [s for s in path[0][i + 1:] if "ROUTPOINT" not in s][0]
            if "ROUTPOINT" not in path[0][i + 1]:
                distances[(',').join([lastTopo_before_i, path[0][i + 1]])] = lastTopo_dist + currDist
            else:
                firstTopo_index = path[0].index(firstTopo_after_i)
                # print("firstTopo_index: ",firstTopo_index)
                tmpDist = 0
                # print("sub array: ", path[i+1:firstTopo_index])
                for j in range(i + 1, firstTopo_index):
                    tmpDist = tmpDist + find_distance_of_route(path[0][j], path[0][j + 1], "../Data/routes.json")
                    # print("2nd case: ", path[j], " ", path[j+1], " ", lastTopo_dist ," ", currDist," ", tmpDist)
                distances[(',').join([lastTopo_before_i, firstTopo_after_i])] = lastTopo_dist + currDist + tmpDist
                # print("2nd: ", (',').join([lastTopo_before_i,firstTopo_after_i]), " ", distances[(',').join([lastTopo_before_i,firstTopo_after_i])])
                idx = j + 1
                # print("iterator: ", i," ", j, " ", idx)


#find_node_degree("../Data/routes.json")

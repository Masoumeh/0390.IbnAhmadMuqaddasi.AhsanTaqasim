import json
import geopy
import geopy.distance
import networkx as nx
import math
import geojson
import collections
import createGraphFromJSON as cg


def find_higher_degree_nodes(G, degree):
    higher_degree_nodes = []
    for node in G.nodes():
        if "ROUTPOINT" not in node and "ROUTEPOINT" not in node:
            if G.degree(node) > degree:
                higher_degree_nodes.append(node)
    return higher_degree_nodes


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


def find_coords_of_uri(uri, fileName):
    coords = []
    with open(fileName) as routesFile:
        allData = json.load(routesFile)
        for d in allData['features']:
            if d['properties']['cornuData']['cornu_URI'] == uri:
                return [(
                    float(d['properties']['cornuData']['coord_lat']), float(d['properties']['cornuData']['coord_lon'])),
                    d['properties']['cornuData']['region_code']]


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
    return [lat2, lon2]


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



def find_coords(routesFile):
    G = cg.createGraphFromJSON(routesFile)
    high_degree_nodes = find_higher_degree_nodes(G, 3)
    nodes_dist = {}
    pFeatures = []
    lFeatures = []
    uri_coord = {}
    for i in range(len(high_degree_nodes) - 2):
        # for j in high_degree_nodes:
        #     if i != j:
        start = find_coords_of_uri(high_degree_nodes[i], "../Data/places.geojson")[0]
        end = find_coords_of_uri(high_degree_nodes[i + 1], "../Data/places.geojson")[0]
        start_end_distance = getPathLength(start[0], start[1], end[0], end[1])
        # nodes_dist[(',').join([high_degree_nodes[i], high_degree_nodes[i + 1]])] = start_end_distance
        no_path = False
        try:
            sh_paths_len = nx.shortest_path_length(G, source=high_degree_nodes[i], target=high_degree_nodes[i+1], weight='length')
            print(high_degree_nodes[i], " ", high_degree_nodes[i + 1], " ", sh_paths_len)
        except nx.NetworkXNoPath:
            no_path = True
            # print(high_degree_nodes[i]," no Path ", high_degree_nodes[i+1])
        if no_path == False:
            nodes_dist[(',').join([high_degree_nodes[i], high_degree_nodes[i + 1]])] = sh_paths_len
    # sorted_nodes_dist = sorted(nodes_dist.items(), key=lambda x: x[1])
    # print(nodes_dist,"          ", sorted_nodes_dist)
    # return
    for sorted_node in nodes_dist:
        if nodes_dist[sorted_node] > 100000:
            continue

        nodes = sorted_node.split(",")
        allpaths = nx.all_shortest_paths(G, source=nodes[0], target=nodes[1], weight='length')
        new_all_path = list(allpaths)
        for path in new_all_path:
            distances = {}
            idx = None
            startData = find_coords_of_uri(path[0], "../Data/places.geojson")
            start = startData[0]
            startReg = startData[1]
            endData = find_coords_of_uri(path[-1], "../Data/places.geojson")
            end = endData[0]
            endReg = endData[1]
            start_end_bearing = calculate_initial_compass_bearing(start, end)
            for i in range(len(path) - 1):
                if idx and i < idx:
                    continue
                if "ROUTPOINT" not in path[i]:
                    tmpStr = (',').join([path[i], path[i + 1]])
                    distances[tmpStr] = find_distance_of_route(path[i], path[i + 1], "../Data/routes.json")
                if "ROUTPOINT" in path[i]:
                    # the last toponym in the array, which is not ROUTPOINT, before the current accurance of ROUTPOINT in array
                    lastTopo_before_i = [s for s in path[:i] if "ROUTPOINT" not in s][-1]
                    # get the distance value for the corresponding route section
                    lastTopo_dist = next(
                        v for k, v in distances.items() if all(x in k for x in [lastTopo_before_i, path[i]]))
                    currDist = find_distance_of_route(path[i], path[i + 1], "../Data/routes.json")
                    if (',').join([lastTopo_before_i, path[i]]) in distances:
                        del distances[(',').join([lastTopo_before_i, path[i]])]

                    # the first toponym in the array, which is not ROUTPOINT, after the current accurance of ROUTPOINT in array
                    firstTopo_after_i = [s for s in path[i + 1:] if "ROUTPOINT" not in s][0]
                    if "ROUTPOINT" not in path[i + 1]:
                        distances[(',').join([lastTopo_before_i, path[i + 1]])] = lastTopo_dist + currDist
                    else:
                        firstTopo_index = path.index(firstTopo_after_i)
                        # print("firstTopo_index: ",firstTopo_index)
                        tmpDist = 0
                        # print("sub array: ", path[i+1:firstTopo_index])
                        for j in range(i + 1, firstTopo_index):
                            tmpDist = tmpDist + find_distance_of_route(path[j], path[j + 1],
                                                                       "../Data/routes.json")
                            # print("2nd case: ", path[j], " ", path[j+1], " ", lastTopo_dist ," ", currDist," ", tmpDist)
                        distances[
                            (',').join([lastTopo_before_i, firstTopo_after_i])] = lastTopo_dist + currDist + tmpDist
                        # print("2nd: ", (',').join([lastTopo_before_i,firstTopo_after_i]), " ", distances[(',').join([lastTopo_before_i,firstTopo_after_i])])
                        idx = j + 1
                        # print("iterator: ", i," ", j, " ", idx)


                        # j = np.where("ROUTPOINT" not in path[:i])
            sum_dist = 0
            for dist in distances:
                sum_dist += distances[dist]
            # print("sum dist: ", sum_dist)
            start_feature = geojson.Feature(geometry=geojson.Point((start[1], start[0])),
                                            properties={'URI': path[0], "region": startReg})
            end_feature = geojson.Feature(geometry=geojson.Point((end[1], end[0])),
                                          properties={'URI': path[-1], "region": endReg})
            start_end_line = geojson.Feature(geometry=geojson.LineString([(start[1], start[0]), (end[1], end[0])]),
                                             properties={'s': path[0], 'e': path[-1]})
            if start_feature not in pFeatures:
                pFeatures.append(start_feature)
            lFeatures.append(start_end_line)

            uri_coord[path[0]] = [start[0], start[1]]
            # uri_coord[path[-1]] = [end[1], end[0]]
            # print(uri_coord)
            # coords.append(list(start))
            for i in range(len(path) - 3):
                topo_to_coordinate = ""
                if "ROUTPOINT" not in path[i] and path[i + 1] not in uri_coord:
                    if "ROUTPOINT" not in path[i + 1]:
                        topo_to_coordinate = path[i + 1]
                        # print("if: ", topo_to_coordinate)
                        d = next(v for k, v in distances.items() if all(x in k for x in [path[i], path[i + 1]]))
                    else:
                        topo_to_coordinate = next(s for s in path[i + 1:] if "ROUTPOINT" not in s)
                        # print("else: ", topo_to_coordinate)
                        d = next(
                            v for k, v in distances.items() if all(x in k for x in [path[i], topo_to_coordinate]))
                    prop_d = (float(d) * float(start_end_distance)) / float(sum_dist)
                    # d = geopy.distance.VincentyDistance(kilometers = prop_d/1000)
                    point = uri_coord[path[i]]
                    # print("topo To: ", topo_to_coordinate)
                    # lat_lon = d.destination(point=point, bearing=start_end_bearing)
                    lat_lon = find_intermediate_coord(prop_d, start_end_bearing, point[0], point[1])
                    uri_coord[topo_to_coordinate] = [lat_lon[0], lat_lon[1]]
                    properties = {'URI': topo_to_coordinate, 'status': 'new',
                                  'region': find_coords_of_uri(topo_to_coordinate, "../Data/places.geojson")[1]}
                    tmp_pFeature = geojson.Feature(geometry=geojson.Point((lat_lon[1], lat_lon[0])),
                                                   properties=properties)
                    tmp_lFeature = geojson.Feature(
                        geometry=geojson.LineString([(uri_coord[path[i]][1], uri_coord[path[i]][0]),
                                                     (lat_lon[1], lat_lon[0])]),
                        properties={'s': path[i], 'e': topo_to_coordinate})
                    pFeatures.append(tmp_pFeature)
                    lFeatures.append(tmp_lFeature)
                    geojson.FeatureCollection(pFeatures)
                    geojson.FeatureCollection(lFeatures)
            # print("uri cords: ", uri_coord)
            if end_feature not in pFeatures:
                pFeatures.append(end_feature)
    pf = geojson.FeatureCollection(pFeatures)
    lf = geojson.FeatureCollection(lFeatures)
    with open("../Data/simplified_cornu_coords_with_distances.geojson", 'w') as outfile:
        geojson.dump(pf, outfile, indent=4, ensure_ascii=False)

find_coords("../Data/routes.json")

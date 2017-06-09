import networkx as nx



def createGraphFromJSON(json_routes):
    """
    Create graph form JSON
    :param json_routes: The json object containing route networks
    :return: The graph computed from route networks
    """
    G = nx.Graph()
    for d in json_routes['features']:
        G.add_node(d['properties']['sToponym'], lat="TBA", lng="TBA", status="old")
        G.add_node(d['properties']['eToponym'], lat="TBA", lng="TBA", status="old")
        G.add_edge(d['properties']['sToponym'], d['properties']['eToponym'], length=d['properties']['Meter'])
    return G


def find_distance_of_route(start, end, json_data):
    """ Find the distance of a route
    :param start: Start Toponym
    :param end: End Toponym
    :param json_data: The JSON data containing all routes
    :return: The distance of the route containing the start and end toponyms
    """
    for d in json_data['features']:
        if (d['properties']['sToponym'] == start and d['properties']['eToponym'] == end) or (
                        d['properties']['sToponym'] == end and d['properties']['eToponym'] == start):
            return d['properties']['Meter']

def find_distance_of_route_t(start, end, json_data):
    """ Find the distance of a route
    :param start: Start Toponym
    :param end: End Toponym
    :param json_data: The JSON data containing all routes
    :return: The distance of the route containing the start and end toponyms
    """
    for d in json_data:
        start_end_list = [d.split("+")[0], json_data[d]['start']['URI'], d.split("+")[1], json_data[d]['end']['URI']]
        if start in start_end_list and end in start_end_list:
            # if start in tmp_list and end in tmp_list:
            return json_data[d]['basic_value'] if json_data[d]['basic_value'] != "null" else 1.0
            # return json_data[d]['cornu_meter'] if json_data[d]['cornu_meter'] != "null" else 37987.00561797753
def find_coords_of_uri(uri, json_data):
    """
    Finds the coordinates of a URI
    :param uri: Toponym
    :param json_data: The JSON data containing all features
    :return: The coordinate of URI
    """
    for d in json_data['features']:
        if d['properties']['cornuData']['cornu_URI'] == uri:
            return [(
                float(d['properties']['cornuData']['coord_lat']),
                float(d['properties']['cornuData']['coord_lon'])),
                d['properties']['cornuData']['region_code']]
    return "NA"


def iterative_bfs(graph, start, deg):
    bfs_res = nx.bfs_edges(graph, start)
    bfs_pre = nx.bfs_predecessors(graph, start)
    found_so_far = []
    found = 0
    start_nexts = {}
    neigh = graph.neighbors(start)
    neigh_proccessed = set()

    for key in bfs_res:
        if len(found_so_far) > graph.degree(start) + 2:
            # if all(item in neigh for item in neigh_proccessed) and len(neigh_proccessed) == len(neigh):
            return found_so_far
        # if "ROUTPOINT" in key[0]:
        #     continue
        if graph.degree(key[1]) == 1 and key[1] not in found_so_far:
            found_so_far.append(key[1])

        if (key[0] != start and graph.degree(key[0]) <= deg) or "ROUTPOINT" in key[0]:
            continue
        val = key[0]
        is_parent_with_high_deg = False
        while val != start:
            if bfs_pre[val] != start and graph.degree(bfs_pre[val]) > deg and "ROUTPOINT" not in bfs_pre[val]:
                is_parent_with_high_deg = True
                break
            val = bfs_pre[val]

        if is_parent_with_high_deg:
            continue
        if key[0] != start and graph.degree(key[0]) > deg and "ROUTPOINT" not in key[
            0] and not is_parent_with_high_deg:
            if key[0] not in found_so_far:
                found_so_far.append(key[0])
        if key[0] == start and graph.degree(key[1]) > deg and "ROUTPOINT" not in key[1]:
            if key[1] not in found_so_far:
                found_so_far.append(key[1])
    return found_so_far

def bfs_for_postprocess(graph, start, deg, simplified_uris, new_coords, json_uris):
    bfs_res = nx.bfs_edges(graph, start)
    bfs_pre = nx.bfs_predecessors(graph, start)
    found_so_far = []
    found = 0
    start_nexts = {}
    neigh = graph.neighbors(start)
    neigh_proccessed = set()

    for key in bfs_res:
        # print("key: ", key)
        if len(found_so_far) > graph.degree(start):
            # if all(item in neigh for item in neigh_proccessed) and len(neigh_proccessed) == len(neigh):
            return found_so_far
        # if "ROUTPOINT" in key[0]:
        #     continue
        # TODO: what to do here??
        # if graph.degree(key[1]) == 1 and key[1] not in found_so_far:
        #     found_so_far.append(key[1])
        key_coords = find_coords_of_uri(key[0], json_uris)
        # print("key coords: ", key_coords)
        if key[0] != start and graph.degree(key[0]) <= deg:
            # print("key0: ", key[0] != start)
            # print('key deg: ', graph.degree(key[0]))
            # print("first not!")
            continue
        if (key[0] != start and graph.degree(key[0]) > deg):
            # print("key0 whd: ", key[0] != start)
            # print('key deg hd: ', graph.degree(key[0]))
            # print('key in sim.new: ', key[0] not in [simplified_uris, new_coords])
            # print('key == na: ', key[0] == "NA")

            if key[0] not in [simplified_uris, new_coords] and key_coords == "NA":
                # print("high deg no uri: ")
                continue
            else:
                val = key[0]
                is_parent_with_high_deg = False
                while val != start:
                    if bfs_pre[val] != start and graph.degree(bfs_pre[val]) > deg \
                            and (bfs_pre[val] in [simplified_uris, new_coords] \
                            or find_coords_of_uri(bfs_pre[val], json_uris) != "NA"):
                        is_parent_with_high_deg = True
                        break
                    val = bfs_pre[val]

                if is_parent_with_high_deg:
                    # print("has parent")
                    continue
            if not is_parent_with_high_deg:
                if key[0] not in found_so_far:
                    # print("key0 should be added")
                    found_so_far.append(key[0])
        if key[0] == start and graph.degree(key[1]) > deg \
                and (key[1] in [simplified_uris, new_coords] or find_coords_of_uri(key[1], json_uris) != "NA"):
            if key[1] not in found_so_far:
                # print("key0 should be added")
                found_so_far.append(key[1])
        # print("found_sofar: ", found_so_far)
    return found_so_far

def find_path_distance(distances, idx, path, json_data_route):
    # f = open("../Data/routes.json", 'r')
    # json_data = json.load(f)
    for i in range(len(path) - 1):
        if idx and i < idx:
            continue
        # if "ROUTPOINT" not in path[0][i]:
        if "ROUTPOINT" not in path[i]:
            tmpStr = (',').join([path[i], path[i + 1]])
            # TODO: generalize for both networks
            distances[tmpStr] = find_distance_of_route(path[i], path[i + 1], json_data_route)
            # distances[tmpStr] = find_distance_of_route_t(path[0][i], path[0][i + 1], json_data_route)
            # distances[tmpStr] = find_distance_of_route_t(path[i], path[i + 1], json_data_route)

        if "ROUTPOINT" in path[i]:
            # the last toponym in the array, which is not ROUTPOINT, before the current accurance of ROUTPOINT in array
            lastTopo_before_i = [s for s in path[:i] if "ROUTPOINT" not in s][-1]
            # get the distance value for the corresponding route section
            lastTopo_dist = next(
                v for k, v in distances.items() if all(x in k for x in [lastTopo_before_i, path[i]]))
            currDist = find_distance_of_route(path[i], path[i + 1], json_data_route)
            if (',').join([lastTopo_before_i, path[i]]) in distances:
                del distances[(',').join([lastTopo_before_i, path[i]])]

            # the first toponym in the array, which is not ROUTPOINT, after the current accurance of ROUTPOINT in array
            firstTopo_after_i = [s for s in path[i + 1:] if "ROUTPOINT" not in s][0]
            if "ROUTPOINT" not in path[i + 1]:
                distances[(',').join([lastTopo_before_i, path[i + 1]])] = lastTopo_dist + currDist
            else:
                firstTopo_index = path.index(firstTopo_after_i)
                tmpDist = 0
                for j in range(i + 1, firstTopo_index):
                    tmpDist = tmpDist + find_distance_of_route(path[j], path[j + 1], json_data_route)
                distances[(',').join([lastTopo_before_i, firstTopo_after_i])] = lastTopo_dist + currDist + tmpDist
                idx = j + 1

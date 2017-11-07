import csv, json

topos = set()
with open("../Data/tripleRoutes_with_meter_basic_values") as muqFile:
    allData = json.load(muqFile)
    with open("../Data/muq_nodes_list", "w") as nodesFile:
        fieldnames = ['node', 'lat', 'lon', 'URI', 'region']
        writer = csv.DictWriter(nodesFile, delimiter="\t", fieldnames=fieldnames, quoting=csv.QUOTE_NONE)
        writer.writeheader()
        for d in allData:
            tmp = d.split("+")
            s = tmp[0]
            e = tmp[1]
            if s not in topos:
                topos.add(s)
                s_tmp = s.split(",")
                s_topo = s_tmp[0]

                s_reg = s_tmp[1:]
                s_lat = allData[d]["start"]["lat"]
                s_lon = allData[d]["start"]["lon"]
                s_uri = allData[d]["start"]["URI"]
                writer.writerow({'node': s_topo, 'lat': s_lat, 'lon': s_lon, 'URI': s_uri, 'region': s_reg})
            else:
                print(s)
            if e not in topos:
                topos.add(e)
                e_tmp = e.split(",")
                e_topo = e_tmp[0]
                e_reg = e_tmp[1:]
                e_lat = allData[d]["end"]["lat"]
                e_lon = allData[d]["end"]["lon"]
                e_uri = allData[d]["end"]["URI"]
                writer.writerow({'node': e_topo, 'lat': e_lat, 'lon': e_lon, 'URI': e_uri, 'region': e_reg})
            else:
                print(e)



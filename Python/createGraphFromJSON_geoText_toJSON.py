from networkx.readwrite import json_graph
import re, json
import networkx as nx
import global_var as gv


def create_graph(geoRoutesFile):
      G = nx.Graph()
  # Add from Muqaddasi
  #  with open(geoRoutesFile, 'r') as grFile:
  #     distReader = json.load(grFile)
      distReader = geoRoutesFile
      for r in distReader:
            startURI = distReader[r]['start']['URI']
            if startURI == 'null' and r.split("+")[0] in gv.found_URIs:
                if re.match(r'\d', gv.found_URIs[r.split("+")[0]]) == None:
                    startURI = gv.found_URIs[r.split("+")[0]]
            startReg = distReader[r]['start']['region']
            startNode = startURI if startURI != "null" else r.split("+")[0]# startURI + "," + startReg if startURI != "null" else r.split("+")[0]
            endURI = distReader[r]['end']['URI']
            if endURI == 'null' and r.split("+")[1] in gv.found_URIs:
                if re.match(r'\d', gv.found_URIs[r.split("+")[1]]) == None:
                    endURI = gv.found_URIs[r.split("+")[1]]
            endReg = distReader[r]['end']['region']
            endNode = endURI if endURI != "null" else r.split("+")[1]# endURI + "," + endReg if endURI != "null" else r.split("+")[1]
            G.add_node(startNode, lat=distReader[r]['start']['lat'], lng=distReader[r]['start']['lon'], status="old" if distReader[r]['start']['URI'] != "null" else "null", region=distReader[r]['start']['region'])
            G.add_node(endNode, lat=distReader[r]['end']['lat'], lng=distReader[r]['end']['lon'], status="old" if distReader[r]['end']['URI'] != "null" else "null", region=distReader[r]['end']['region'])
            # G.add_edge(startNode, endNode, length= distReader[r]['distance'])
            G.add_edge(startNode, endNode, length=float(distReader[r]['basic_value']) if distReader[r]['basic_value'] != "null"
                       else float(1))

   # data = json_graph.node_link_data(G)
   # with open('Muqaddasi_Graph_noNorm_noAL_origkey90.json', 'w') as graphfile:
   #        json.dump(data, graphfile, ensure_ascii=False, indent=4)
   #        print("node: ", node, "-", G.neighbors(node))
   # print(nx.number_connected_components(G))
      return G


# createGraph("../Data/Distances_withCoords_normalized_with_cornuRegion_json_noNorm_noAL_origkey90")
# create_graph("../Data/tripleRoutes_with_basic_values")
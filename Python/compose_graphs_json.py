from networkx.readwrite import json_graph
import json
import networkx as nx


def composeGraphs(geoRoutesFile, jsonFile, cornuPlaces):
   G = nx.Graph()
  # Add from Muqaddasi
   with open(geoRoutesFile, 'r') as grFile:
      distReader = json.load(grFile)
      for r in distReader:
        startURI = distReader[r]['start']['URI']
        startReg = distReader[r]['start']['region']
        startNode = startURI + "," + startReg if startURI != "null" else r.split("+")[0] 
        endURI = distReader[r]['end']['URI']
        endReg = distReader[r]['end']['region']
        endNode = endURI + "," + endReg if endURI != "null" else r.split("+")[1]
        #print(tmpNode1)
        G.add_node(startNode, lat= distReader[r]['start']['lat'], lng= distReader[r]['start']['lon'], status="old" if distReader[r]['start']['URI'] != "null" else "null", region=distReader[r]['start']['region'])
        #print(tmpNode2)
        G.add_node(endNode, lat= distReader[r]['end']['lat'], lng= distReader[r]['end']['lon'], status="old" if distReader[r]['end']['URI'] != "null" else "null", region=distReader[r]['end']['region'])
        G.add_edge(startNode, endNode, length= distReader[r]['cornu_meter'])

  # Add more from Cornu
   with open(jsonFile) as tmpFile2:    
      allData = json.load(tmpFile2)
      for d in allData['features']:
        if "ROUT" in d['properties']['sToponym'] + d['properties']['eToponym']:
          continue
        if d['properties']['sToponym'] not in G.nodes():
          with open(cornuPlaces) as cornuFile:    
            places = json.load(cornuFile)
            for p in places['features']:
              if p['properties']['cornuData']['cornu_URI'] == d['properties']['sToponym']:
                G.add_node(d['properties']['sToponym']+ ","+p['properties']['cornuData']['region_code'], lat = p['properties']['cornuData']['coord_lat'], lng=p['properties']['cornuData']['coord_lon'], status="old", region=p['properties']['cornuData']['region_code'])
        if d['properties']['eToponym'] not in G.nodes():
          with open(cornuPlaces) as cornuFile:    
            places = json.load(cornuFile)
            for p in places['features']:
              if p['properties']['cornuData']['cornu_URI'] == d['properties']['eToponym']:
                G.add_node(d['properties']['eToponym']+ ","+p['properties']['cornuData']['region_code'], lat = p['properties']['cornuData']['coord_lat'], lng=p['properties']['cornuData']['coord_lon'], status="old", region=p['properties']['cornuData']['region_code'])
        if d['properties']['sToponym'] in G.nodes() and d['properties']['eToponym'] in G.nodes():
          G.add_edge(d['properties']['sToponym'] ,d['properties']['eToponym'], length= d['properties']['Meter'])
   data = json_graph.node_link_data(G)
   with open('composedGraph_json2.json', 'w') as graphfile:
          json.dump(data, graphfile, ensure_ascii=False, indent=4) 
   return G

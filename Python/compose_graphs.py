'''
Create a graph of both cornu and muqaddasi networks and writes the graph into a json file.
'''

from networkx.readwrite import json_graph
import io, json, csv
import re
import networkx as nx
import matplotlib.pyplot as plt	
import sys  
import math
from decimal import *
from pyproj import *


def composeGraphs(csvFile, jsonFile, cornuPlaces):
   G = nx.Graph()
  # Add from Muqaddasi
   with open(csvFile, 'r') as tmpFile:
      distReader = csv.reader(tmpFile, delimiter=',')
      next(distReader, None)
      for row in distReader:
        #print(row)
        #print(row[0], "-", row[1],"-", row[2], "-",row[3],"-", row[4],"-", row[5],"-", row[6],"-", row[7], "-",row[8], "-", row[9])
        # this line splite the row if it has array of regions from Muqaddasi text included, like below:
        #الزيتونة,"34.35352,10.10538,['Maghrib', 'Barqa', 'Andalus'],ZAYTUNA_101E343N_S",كتانة,"33.69175,10.27879,['Maghrib', 'Barqa', 'Andalus'],KATANA_102E336N_S",مرحلة
        #splitRow = re.split(',"|,[|],|",',row)
        '''splitRow = re.split(',"|",', row) 
# ['ذات عرق', '21.62677,40.42853,Jazirat al-Arab,DHATIRQ_404E216N_S', 'الغمرة', '						21.89675,40.84007,Jazirat al-Arab,GHAMRA_408E218N_S', 'مرحلة']
        startInfo = re.split(',',splitRow[1]) 
	# '21.62677,40.42853,Jazirat al-Arab,DHATIRQ_404E216N_S'
        endInfo = re.split(',',splitRow[3])   
	# '21.89675,40.84007,Jazirat al-Arab,GHAMRA_408E218N_S'
        #print(endInfo)
        start = splitRow[0]
                   
# ذات عرق
        startLat = startInfo.split(',')[0]
        startLng = startInfo.split(',')[1]
        startReg = startInfo.split(',')[2]
        startUri = startInfo.split(',')[-1]
        end = splitRow[2]                     
# الغمرة
        endLat = endInfo.split(',')[0]
        endLng = endInfo.split(',')[1]
        endReg = endInfo.split(',')[2]
        endUri = endInfo.split(',')[-1]       
        distance = splitRow[-1]'''
        tmpNode1 = row[4].strip('"')+"-"+row[3] if row[4].strip('"') != "null" else row[0]+"-"+row[3]
        #print(tmpNode1)
        G.add_node(tmpNode1, lat=row[1], lng=row[2], status="old" if row[1] != "null" and row[2] != "null" else "null", region=row[3])
        tmpNode2 = row[9].strip('"')+"-"+row[8] if row[9].strip('"') != "null" else row[5]+"-"+row[8]
        #print(tmpNode2)
        G.add_node(tmpNode2, lat=row[6], lng=row[7], status="old" if row[6] != "null" and row[7] != "null" else "null", region=row[8])
        G.add_edge(tmpNode1, tmpNode2, length= row[10])

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
                G.add_node(d['properties']['sToponym']+ "-"+p['properties']['cornuData']['region_code'], lat = p['properties']['cornuData']['coord_lat'], lng=p['properties']['cornuData']['coord_lon'], status="old", region=p['properties']['cornuData']['region_code'])
                #break
                #print("stopo: ", d['properties']['sToponym']+ "-"+p['properties']['cornuData']['region_code'])
                '''print("sTOPO: " ,d['properties']['sToponym'])
                print( "lat=" , p['properties']['cornuData']['coord_lat'])
                print( "lng=" ,p['properties']['cornuData']['coord_lon'])
                print("region=",p['properties']['cornuData']['region_code']'''
        if d['properties']['eToponym'] not in G.nodes():
          with open(cornuPlaces) as cornuFile:    
            places = json.load(cornuFile)
            for p in places['features']:
              if p['properties']['cornuData']['cornu_URI'] == d['properties']['eToponym']:
                G.add_node(d['properties']['eToponym']+ "-"+p['properties']['cornuData']['region_code'], lat = p['properties']['cornuData']['coord_lat'], lng=p['properties']['cornuData']['coord_lon'], status="old", region=p['properties']['cornuData']['region_code'])
                #break
                #print("etopo: ", d['properties']['eToponym']+ "-"+p['properties']['cornuData']['region_code'])
                '''print("eTOPO: " ,d['properties']['eToponym'])
                print( "lat=" , p['properties']['cornuData']['coord_lat'])
                print( "lng=" ,p['properties']['cornuData']['coord_lon'])
                print("region=",p['properties']['cornuData']['region_code'])
                #print(node)'''
        if d['properties']['sToponym'] in G.nodes() and d['properties']['eToponym'] in G.nodes():
          G.add_edge(d['properties']['sToponym'] ,d['properties']['eToponym'], length= d['properties']['Meter'])
   data = json_graph.node_link_data(G)
   with open('composedGraph2.json', 'w') as graphfile:
          json.dump(data, graphfile, ensure_ascii=False, indent=4) 
   return G

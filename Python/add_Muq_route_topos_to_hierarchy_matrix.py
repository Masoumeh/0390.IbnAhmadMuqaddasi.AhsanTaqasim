"""
Create Matrix for cornu data in two levels (regions and settlements)
"""
import csv, json
import io
import scipy.sparse as sps
import numpy as np
import pandas as pd
import pprint 


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


def add_route_topos (geoRoutes, geoMatrix):
  with open(geoRoutes, "r", encoding="utf8") as routes:
      routes = json.load(routes)
      for r in routes:
        start_topo = r.split("+")[0].split(",")[0]
        start_URI =  r['start']['URI']
        sReg = ','.join(r.split("+")[0].split(",")[1:])
        end_topo = r.split("+")[1].split(",")[0]
        end_URI =  r['end']['URI']
        eReg = ','.join(r.split("+")[1].split(",")[1:])
        with open(geoMatrix, "r", encoding="utf8") as matrix:
          matrix = json.load(matrix)
          if start_URI != 'null' and start_URI not in matrix[sReg]:
            matrix[sReg][start_URI] = 1
          if end_URI != 'null' and end_URI not in matrix[eReg]:
            matrix[eReg][end_URI] = 1
          if start_URI == 'null':
            


add_route_topos ("../Data/Distances_withCoords_normalized_with_cornuRegion_json_noNorm_noAL_origkey90")

"""
Flatten the structure of all shortest paths (Muqaddasi route network) to a list of paths.
"""

import json
import csv


def flatten_file_struct(muq_routes_file, write_file):
  with open(muq_routes_file) as jsonFile:    
      all_routes = json.load(jsonFile)
      with open (write_file, 'w') as pathsList:
        fWriter = csv.writer(pathsList, delimiter=',')
        for r in all_routes:
          for d in all_routes[r]:
             fWriter.writerow(all_routes[r][d])
        

process("Muqaddasi_all_shortest_paths.json", "Muqaddasi_all_shortest_paths.csv")
print("done")

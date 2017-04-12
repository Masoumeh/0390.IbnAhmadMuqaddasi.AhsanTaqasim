"""
Process shortest paths (Muqaddasi route network) to remove the duplicate paths.
"""

import csv
import itertools
import io
import re

def process(muq_routes_file):
  '''with open(muq_routes_file, "r") as f:
        for line in f:
        for p1 in reader:
          for P2 in reader:
            print(reader[ip])'''
  outfile = open("Muqaddasi_all_shortest_paths_noDuplicates.txt", "w")
  lines_to_check_for = [ line for line in open(muq_routes_file, "r") ]
  #print(lines_to_check_for)
  found = False
  for line in open(muq_routes_file, "r"):
    found = False
    tmp = line.split('","')
    tmp[:] = [re.sub('"|\n', '', t ) for t in tmp]
    for l in lines_to_check_for:
      if l != line:
        if all(x in l for x in tmp): #can use intersection of sets as well
          found = True
          break
    if found == False:
        outfile.write(line)
   
        

process("Muqaddasi_all_shortest_paths.csv")
print("done")

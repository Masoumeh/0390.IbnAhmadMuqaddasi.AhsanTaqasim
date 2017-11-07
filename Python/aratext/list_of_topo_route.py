import csv
import re
import pandas as pan
from itertools import *
from itertools import *


def extract_list_of_topo(tri_file, singles_file, compounds_file):
    topos_single = []
    topos_compound = []
    tri_f = open(tri_file, "r")
    tri = pan.read_csv(tri_f, names=["from","to","distance"], delimiter="\t")
    for i,t in islice(tri.iterrows(), 1, None):
        f = t['from'].strip()
        to = t['to'].strip()
        if len(f.split(" ")) <= 1 and f not in topos_single:
            topos_single.append(f)
        if len(f.split(" ")) > 1 and f not in topos_compound:
            topos_compound.append(f)
        if len(to.split(" ")) <= 1 and to not in topos_single:
            topos_single.append(to)
        if len(to.split(" ")) > 1 and to not in topos_compound:
            # print("ct: ", to)
            # len(to.split(" "))
            topos_compound.append(to)
    with open(singles_file, "w") as out1:
        # writer = csv.writer(out1)
        # for s in topos_single:
        out1.write(("\n").join(topos_single))
    with open(compounds_file, "w") as out2:
        writer = csv.writer(out2)
        # for c in topos_compound:
        out2.write(("\n").join(topos_compound))




extract_list_of_topo("/home/rostam/Desktop/Chiara/It.Ant. - tagged_new_tri",
                     "/home/rostam/Desktop/Chiara/It.Ant. - tagged_new_sTopoList",
                     "/home/rostam/Desktop/Chiara/It.Ant. - tagged_new_cTopoList")
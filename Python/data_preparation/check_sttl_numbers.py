"""
checks the number of sttls in both triples file and hierarchy files,
in order to find any missing stl in hierarchy- the number of sttl in triples file is bigger than hierarchy file.
"""

import csv

def get_sttl_with_reg(triple_file, hier_file):
    """
    :param fileN_name: The name of csv file containing hierarchies from PROV to STTL. 
    :return: returns a list of settlements together with their province (the highest level region), 
    concatenated with "-" as one string, e.g. البصرة-العراق
    """
    # Set of names together with latest region and province
    tri_sttl = []
    hier_sttl = []
    tri_f = open(triple_file, "r", encoding="utf8")
    hier_f = open(hier_file, "r", encoding="utf8")
    tri = csv.reader(tri_f, delimiter="\t")
    hier = csv.reader(hier_f, delimiter=",")
    w_t = open("sttls_t", "w")
    writer_t = csv.writer(w_t, delimiter='\t')
    w_h = open("sttls_h", "w")
    writer_h = csv.writer(w_h, delimiter='\t')
    dup_t = []
    dup_h = []
    for t in tri:
        if t[-1].startswith("STTL"):
            if t[-1][4:].strip() in tri_sttl:
                dup_t.append(t[-1][4:])
            else:
                tri_sttl.append(t[-1][4:].strip())
    for h in hier:
        if h[-1].startswith("STTL"):
            if h[-1][4:].strip() in hier_sttl:
                dup_h.append(h[-1][4:])
            else:
                hier_sttl.append(h[-1][4:].strip())
    print(len(dup_t))
    print(len(dup_h))
    print([item for item in dup_h if item in dup_t])
    print([item for item in dup_t if item not in dup_h])
    print([item for item in dup_h if item not in dup_t])
    # print(dup_t)
    # print(dup_h)

    # for t in tri_sttl:
    #     writer_t.writerow(t)
    #
    # for h in hier_sttl:
    #     writer_h.writerow(h)



get_sttl_with_reg("/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_triples_hier",
                  "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_hier_all")

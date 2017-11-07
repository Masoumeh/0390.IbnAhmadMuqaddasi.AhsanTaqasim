"""
Return a lis of settlements in a hierarchy.
"""
def get_sttl_with_reg(file_name):
    """
    Makes a list of sttl names with region and province. 
    :param fileN_name: The name of csv file containing hierarchies from PROV to STTL. 
    :return: returns a list of settlements together with their province (the highest level region), 
    concatenated with "-" as one string, e.g. البصرة-العراق
    """
    # Set of names together with latest region and province
    names = set()
    with open(file_name, "r", encoding="utf8") as f1:
        f1 = f1.read().split("\n")
        tmp = ""
        cnt = 0
        for l in f1:
          cnt = cnt + 1
          ls = l.split(",")
          if ls[-1].startswith("STTL"):
            # join the sttl name with latest region and province to which it belongs
            # tmp = "-".join((ls[-1][4:].strip(), ls[0][4:].strip(), ls[-3][4:].strip()))
            # join the sttl name with the province to which it belongs
            # if ls[-1][4:].strip().startswith("STTL"):
            tmp = "/".join((ls[-1][4:].strip(), ls[0][4:].strip(), ls[-3][4:].strip()))
            if tmp in names:
                print(tmp)
            else:
                names.add(tmp)
    print("name count: ", len(names))
    return names

def get_sttl(file_name):
    """
    Makes a list of sttl names without region and province. 
    :param fileN_name: The name of csv file containing hierarchies from PROV to STTL. 
    :return: returns a list of settlements 
    """
    # Set of names together with latest region and province
    names = set()
    with open(file_name, "r", encoding="utf8") as f1:
        f1 = f1.read().split("\n")
        tmp = ""
        cnt = 0
        for l in f1:
          cnt = cnt + 1
          ls = l.split(",")
          if ls[-1].startswith("STTL"):
            # join the sttl name with latest region and province to which it belongs
            # tmp = "-".join((ls[-1][4:].strip(), ls[0][4:].strip(), ls[-3][4:].strip()))
            # join the sttl name with the province to which it belongs
            # if ls[-1][4:].strip().startswith("STTL"):
            # tmp = "/".join((ls[-1][4:].strip(), ls[0][4:].strip(), ls[-3][4:].strip()))
            if ls[-1] in names:
                print(tmp)
            else:
                names.add(ls[-1][4:].strip())
    # print(names)
    # print("name count: ", len(names))
    return names

# get_sttl("/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/Muqaddasi/muq_hier_all")

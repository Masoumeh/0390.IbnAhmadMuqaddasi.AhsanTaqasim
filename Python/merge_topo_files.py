import csv
import pandas as pan
from itertools import *

def merge(topo_mic, topo_mes, topo_mac, merged_topos):
    micro = open (topo_mic, "r")
    topos_mic = pan.read_csv(micro, delimiter='\t', names=["URI", "TOP", "TRANSLIT", "TYPE", "LAT", "LON", "REG_MESO"])

    meso = open(topo_mes, "r")
    topos_mes = pan.read_csv(meso, delimiter='\t', names=["REG_MESO", "LAT", "LON", "COLOR", "REG_MACRO"])

    macro = open(topo_mac, "r")
    topos_mac = pan.read_csv(macro, delimiter="\t", names=["REG_MACRO", "LAT", "LON", "COLOR"])
    with open(merged_topos, "w") as out_file:
        headers = ["URI", "TOP", "TRANSLIT", "TYPE", "LAT", "LON", "REG_MESO", "MESO_LAT", "MESO_LON",
                   "MESO_COLOR", "MACRO", "MACRO_LAT", "MACRO_LON", "MACRO_COLOR"]
        writer = csv.DictWriter(out_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
        writer.writeheader()
        for index, t in islice(topos_mic.iterrows(), 1, None):
            mes_reg = t["REG_MESO"]
            for i, me in islice(topos_mes.iterrows(), 1, None):
                if me["REG_MESO"] == mes_reg:
                   mes_lat = me["LAT"]
                   mes_lon = me["LON"]
                   mes_color = me["COLOR"]
                   mac_reg = me["REG_MACRO"]
                   break
            for i, ma in islice(topos_mac.iterrows(), 1, None):
                if ma["REG_MACRO"] == mac_reg:
                   mac_lat = ma["LAT"]
                   mac_lon = ma["LON"]
                   mac_color = ma["COLOR"]
                   break
            writer.writerow({"URI":t["URI"], "TOP":t["TOP"], "TRANSLIT":t["TRANSLIT"], "TYPE":t["TYPE"],
                             "LAT":t["LAT"], "LON":t["LON"], "REG_MESO":t["REG_MESO"], "MESO_LAT":mes_lat,
                             "MESO_LON":mes_lon, "MESO_COLOR":mes_color, "MACRO":mac_reg, "MACRO_LAT": mac_lat,
                             "MACRO_LON":mac_lon, "MACRO_COLOR":mac_color})



merge("../Data/toponymMicro.csv", "../Data/toponymMeso.csv", "../Data/toponymMacro.csv", "../Data/toponyms.csv")
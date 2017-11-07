import csv, json
import pandas as pan
from itertools import *


def csv_to_json_convertor(csv_file, json_file):
    new_dict = {}
    items = {}
    f = open (csv_file, "r")
    csv = pan.read_csv(f, delimiter="\t", names=["URI", "ITEM", "TRANSLIT", "SEARCH", "TRANSLATION", "CLASSIFIERS",
                                               "COMMENT"])
    for i, r in islice(csv.iterrows(), 1, None):
        # print(r["ITEM"])
      new_dict[r["ITEM"]] = {}
      new_dict[r["ITEM"]]["URI"] = "NaN" if r["URI"] == 'NaN' else r["URI"]
      new_dict[r["ITEM"]]["SEARCH"] = "NaN" if r["SEARCH"] == 'NaN' else r["SEARCH"]
      new_dict[r["ITEM"]]["TRANSLIT"] = "NaN" if r["TRANSLIT"] == 'NaN' else r["TRANSLIT"]
      new_dict[r["ITEM"]]["TRANSLATION"] = "NaN" if r["TRANSLATION"] == 'NaN' else r["TRANSLATION"]
      new_dict[r["ITEM"]]["CLASSIFIERS"] = "NaN" if r["CLASSIFIERS"] == 'NaN' else r["CLASSIFIERS"]
      new_dict[r["ITEM"]]["COMMENT"] = "NaN" if r["COMMENT"] == 'NaN' else r["COMMENT"]
      items.update(new_dict)
    with open(json_file, "w") as out_file:
        json.dump(items, out_file, ensure_ascii=False, indent=4)



csv_to_json_convertor("../Data/descScheme.csv", "../Data/descScheme.json")
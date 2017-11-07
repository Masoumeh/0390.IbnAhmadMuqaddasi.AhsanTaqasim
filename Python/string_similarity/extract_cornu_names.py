import json


def extract_cornu_names():
    cornu_places = "/home/rostam/Arabic_Persian/LocalAlmoghaddasi/Data/places.geojson"
    arr = set()
    with open(cornu_places, "r", encoding="utf8") as json_file:
        cornu_features = json.load(json_file)
        for f in cornu_features["features"]:
            cornu_title = f["properties"]["cornuData"]["toponym_arabic"]
            cornu_title_other = f["properties"]["cornuData"]["toponym_arabic_other"].split("،")
            cornu_reg = f["properties"]["cornuData"]["region_code"]
            if "RoutPoint" not in cornu_title:
                arr.add(cornu_title.strip())
                for c in cornu_title_other:
                    arr.add(c.strip())

    return arr

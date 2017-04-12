import json

colorLookup = {
    #"Andalus": "#323449",
    "Aqur": "#A768E6",
    "Barqa": "#58E0C1",
    "Daylam": "#D5812E",
    "Egypt": "#6CD941",
    "Faris": "#E23A80",
    "Iraq": "#ABB1DB",
    "Jibal": "#384E21",
    "Khazar": "#BDD977",
    "Khurasan": "#B27E86",
    "Khuzistan": "#8F351D",
    "Kirman": "#D5AB7A",
    "Mafaza": "#d3d3d3",#"#514285", has changed to light gray to set this region to background
    "Maghrib": "#539675",
    "Rihab": "#DB4621",
    "Sham": "#539236",
    "Sicile": "#4B281F",
    "Sijistan": "#68DA85",
    "Sind": "#6C7BD8",
    #"Transoxiana": "#DBB540",
    "Yemen": "#8F3247",
    22: "#000000",#"#A8DBD5", has changed to light gray to set this region to background
    "Badiyat al-Arab": "#d3d3d3",#"#C9DB3F", has changed to light gray to set this region to background
    "Jazirat al-Arab": "#537195",
    "NoRegion": "#d3d3d3", # "#7E5C31", for routepoints clearly between regions
    '26': "#D1785F",
    '27': "#898837",
    '28': "#DC4AD3",
    '29': "#DD454F",
    '30': "#C4D9A5",
    '31': "#DDC1BF",
    '32': "#D498D2",
    '33': "#61B7D6",
    '34': "#A357B1",
    "Transoxiana": "#522046",
    '36': '#849389',
    #"Transoxiana": "#3B524B",
    '38': "#DD6F91",
    '39': "#B4368A",
    "Andalus": "#8F547C"
}
def create_new_struct(sourceFile):
    with open(sourceFile) as rFile:
        allData = json.load(rFile)
        featureColl = {}
        featureColl['type'] = "FeatureCollection"
        featureColl['features'] = []
        regions = {}
        for d in allData["features"]:
            if d['properties']['cornuData']['region_code'] not in regions:
                regions[d['properties']['cornuData']['region_code']] = {}
                regions[d['properties']['cornuData']['region_code']]['display'] = d['properties']['cornuData']['region_spelled']
                regions[d['properties']['cornuData']['region_code']]['color'] = colorLookup[d['properties']['cornuData']['region_code']]
                if d['properties']['althurayyaData']['visual_center'] == 'yes':
                    regions[d['properties']['cornuData']['region_code']]['visual_center'] = d['properties']['cornuData']['cornu_URI']
                else:
                    regions[d['properties']['cornuData']['region_code']]['visual_center'] = ""
            elif regions[d['properties']['cornuData']['region_code']]['visual_center'] == "" and d['properties']['althurayyaData']['visual_center'] == 'yes':
                regions[d['properties']['cornuData']['region_code']]['visual_center'] = d['properties']['cornuData']['cornu_URI']
            new_d = {}
            new_d['geometry'] = d['geometry']
            new_d['type'] = d['type']
            new_d['archive'] = {}
            new_d['archive']['cornuData'] = d['properties']['cornuData']
            new_d['properties'] = {}
            new_d['properties']["althurayyaData"] = {}
            # new_d['properties']["althurayyaData"]['sources'] = {}
            # source = {}
            new_d['properties']["althurayyaData"]['source'] = "cornuData"
            new_d['properties']["althurayyaData"]['coord_certainty'] = d['properties']['cornuData']["coord_certainty"]
            new_d['properties']["althurayyaData"]['coord_lat'] = d['properties']['cornuData']["coord_lat"]
            new_d['properties']["althurayyaData"]["coord_lon"] = d['properties']['cornuData']["coord_lon"]
            new_d['properties']["althurayyaData"]["URI"] = d['properties']['cornuData']["cornu_URI"]
            new_d['properties']["althurayyaData"]["region"] = d['properties']['cornuData']['region_code']
            # new_d['properties']["althurayyaData"]["region_code"] = d['properties']['cornuData']['region_code']
            # new_d['properties']["althurayyaData"]["region_spelled"] = d['properties']['cornuData']['region_spelled']
            # new_d['properties']["althurayyaData"]["top_type_hom"] = d['properties']['cornuData']["top_type_hom"]
            new_d['properties']["althurayyaData"]["top_type"] = d['properties']['cornuData']["top_type_hom"]
            # new_d['properties']["althurayyaData"]["original_language"] = ""
            # new_d['properties']["althurayyaData"]["toponym_original"] = d['properties']['cornuData']["toponym_arabic"]
            # new_d['properties']["althurayyaData"]["toponym_original_other"] = d['properties']['cornuData']["toponym_arabic_other"]
            new_d['properties']["althurayyaData"]["names"] = {}
            # name = {}
            # name["arabic"] = {}
            # name["toponym_search"] = d['properties']['cornuData']["toponym_search"]
            # name["toponym_translit"] = d['properties']['cornuData']["toponym_translit"]
            # name["toponym_translit_other"] = d['properties']['cornuData']["toponym_translit_other"]
            new_d['properties']["althurayyaData"]["names"]['arabic'] = {}
            new_d['properties']["althurayyaData"]["names"]['arabic']['search'] = d['properties']['cornuData']["toponym_arabic"]
            new_d['properties']["althurayyaData"]["names"]['arabic']['common'] = d['properties']['cornuData']["toponym_arabic"]
            new_d['properties']["althurayyaData"]["names"]['arabic']['common_other'] = d['properties']['cornuData']["toponym_arabic_other"]
            new_d['properties']["althurayyaData"]["names"]['arabic']['translit'] = ""
            new_d['properties']["althurayyaData"]["names"]['arabic']['translit_other'] = ""
            new_d['properties']["althurayyaData"]["names"]['english'] = {}
            new_d['properties']["althurayyaData"]["names"]['english']['search'] = d['properties']['cornuData'][
                "toponym_search"]
            new_d['properties']["althurayyaData"]["names"]['english']['common'] = ""
            new_d['properties']["althurayyaData"]["names"]['english']['common_other'] = ""
            new_d['properties']["althurayyaData"]["names"]['english']['translit'] = d['properties']['cornuData'][
                "toponym_translit"]
            new_d['properties']["althurayyaData"]["names"]['english']['translit_other'] = d['properties']['cornuData'][
                "toponym_translit_other"]
            # source["names"].update(name)
            # new_d['properties']["althurayyaData"].update(source)
            # new_d['properties']["althurayyaData"]['names'] = name
            new_d['properties']["references"] = {}
            new_d['properties']["references"]["primary"] = {}
            new_d['properties']["references"]["secondary"] = {}
            for k,v in d["properties"]["sources_arabic"].items():
                tmp_ref = {}
                tmp_ref[k] = v
                # tmp_ref[k]['type'] = "primary"
                tmp_ref[k]['match_rate'] = d["properties"]["sources_arabic"][k]['rate']
                tmp_ref[k]['match_status'] = d["properties"]["sources_arabic"][k]['status']
                tmp_ref[k]['language_orig'] = 'Arabic'
                tmp_ref[k]['language_manifestation'] = ''
                del tmp_ref[k]['rate']
                del tmp_ref[k]['status']
                new_d['properties']["references"]['primary'].update(tmp_ref)
            for k,v in d["properties"]["sources_english"].items():
                print(k, " ",v)
                tmp_ref = {}
                tmp_ref[v['uri']] = {}
                # tmp_ref[v['uri']]['type'] = "secondary"
                tmp_ref[v['uri']]['match_rate'] = ""
                tmp_ref[v['uri']]['match_status'] = ""
                tmp_ref[v['uri']]['language_orig'] = 'English'
                tmp_ref[v['uri']]['language_manifestation'] = ''
                # del tmp_ref[v['uri']]['uri']
                new_d['properties']["references"]['secondary'].update(tmp_ref)
            featureColl['features'].append(new_d)

    with open("../Data/places_new_structure.geojson", 'w') as outfile:
        json.dump(featureColl, outfile, sort_keys=True, indent=4, ensure_ascii=False)
    with open("../Data/regions.json", 'w') as outfile:
        json.dump(regions, outfile, sort_keys=True, indent=4, ensure_ascii=False)
create_new_struct("../Data/places.geojson")
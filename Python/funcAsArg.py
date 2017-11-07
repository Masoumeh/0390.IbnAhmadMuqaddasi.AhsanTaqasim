from aratext import normalization as norm
import json, csv, geojson
import global_var as gv

def match(sttl_reg, cornu_feature, cond):
    match_dict = {}
    topo_name = sttl_reg.split("-")[0]
    topo_reg = sttl_reg.split("-")[1]
    cornu_title = cornu_feature["properties"]["cornuData"]["toponym_arabic"]
    cornu_title_other = cornu_feature["properties"]["cornuData"]["toponym_arabic_other"]

    cornu_reg = cornu_feature["properties"]["cornuData"]["region_code"]
    if cond(topo_name,cornu_title,topo_reg, cornu_reg):
        match_dict[sttl_reg] = {}
        match_dict[sttl_reg]["Geo Prov"] = topo_reg
        match_dict[sttl_reg]["Cornu feature"] = cornu_feature
    else:
        for n in cornu_title_other:
            n = n.strip()
            if cond(topo_name,n,topo_reg, cornu_reg):
                match_dict[sttl_reg] = {}
                match_dict[sttl_reg]["Geo Prov"] = topo_reg
                match_dict[sttl_reg]["Cornu feature"] = cornu_feature
    return match_dict if sttl_reg in match_dict else None


def cond_match(topo_name, cornu_title, topo_reg, cornu_reg):
    return norm.normalize_alphabet(topo_name) == norm.normalize_alphabet(cornu_title) and cornu_reg in gv.reg_dict[topo_reg]


match(sttl_reg, cornu_feature, cond_match)
# def cond1(topo_name, cornu_title, topo_reg):
#     fuzz.ratio(norm.normalize_alphabet(topo_name), norm.normalize_alphabet(cornu_title)) >= 90 and \
#         cornu_reg in topo_reg
#
# fuzz.ratio(norm.normalize_alphabet(topo_name), norm.normalize_alphabet(n)) >= 90 and \
#                             cornu_reg in topo_reg
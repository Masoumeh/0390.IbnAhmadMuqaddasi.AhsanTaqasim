import os.path
# from get_sttls_regs import get_sttl_with_reg as gs
import csv
import json
import match_functions as mf
import pandas as pan
from cltk.stem.lemma import LemmaReplacer
from cltk.stem.latin.j_v import JVReplacer
import networkx as nx
from networkx.readwrite import json_graph
from itertools import *


def get_cornu_matches(sttl_names, cornu_places,
                      # the next line should be commented out for hierarchical data
                      # cornu_graph,
                      write_file, match_func, match_status, method, cornu_matched):
    found = []
    file_exists = os.path.isfile(write_file)

    with open(write_file, 'a', encoding="utf8") as matches_file:
        headers = ["Geo Title", "Cornu Title", "Cornu Title Other",
                   # the next line should be commented out for hierarchical data
                   'Geo Neighbours', 'Cornu Neighbours',
                   "lat", "lon", "Cornu Region", "Geo Prov",
                   "Geo Subregion", "Cornu URI", "Status", "Match Method"]
        writer = csv.DictWriter(matches_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
        if not file_exists:
            writer.writeheader()  # file doesn't exist yet, write a header
        with open(cornu_places, "r", encoding="utf8") as json_file:
            cornu_features = json.load(json_file)
            t = type(sttl_names)
            if t == nx.classes.graph.Graph:
                t_type = "graph"
                sttl_list = [s for s in sttl_names.nodes() if len(sttl_names.node[s]['matches']) == 0]
            else:
                t_type = "list"
                sttl_list = sttl_names
            for st in sttl_list:
                # if st not in found_topos:
                # print("st: ", st)
                tmp = mf.find_match(match_func, cornu_features, st, cornu_matched)
                # print("tmp: ", tmp)
                if tmp != None:
                        found.append(st)
                        for t in tmp:
                            # print(st)
                            cornu_data = t[st]["Cornu feature"]["properties"]["cornuData"]
                            cornu_uri = cornu_data["cornu_URI"]
                            writer.writerow({"Geo Title": st.split('/')[0],
                                             'Cornu Title': cornu_data["toponym_arabic"],
                                             'Cornu Title Other': cornu_data["toponym_arabic_other"],
                                             # the next two key,value pairs should be commented out for hierarchical data
                                             # 'Geo Neighbours':
                                             #     # sttl_names.neighbors(st) if t_type == "graph" else
                                             #     "null",
                                             # 'Cornu Neighbours':
                                             #     cornu_graph.neighbors(cornu_uri) if cornu_uri in cornu_graph else "null",
                                             'lat': cornu_data["coord_lat"],
                                             'lon': cornu_data["coord_lon"],
                                             'Cornu Region': cornu_data["region_spelled"], # should be region_code normally
                                             'Geo Prov': st.split('/')[1],
                                             'Geo Subregion': "null" if t_type == "graph" else st.split('/')[2],
                                             'Cornu URI': cornu_uri,
                                             'Status': match_status,
                                             'Match Method': method})
            return found


def get_cornu_route_matches(txt_graph, cornu_places, cornu_graph, write_file, match_func, match_status, method,
                            cornu_matched):
    found = []
    file_exists = os.path.isfile(write_file)

    with open(write_file, 'a', encoding="utf8") as matches_file:
        headers = ["Geo Title", "Cornu Title", "Cornu Title Other", "Cornu Region",
                   "Geo Neighbours", "Cornu Neighbours", "Cornu URI", "lat", "lon", "Status", "Match Method"]
        writer = csv.DictWriter(matches_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
        if not file_exists:
            writer.writeheader()  # file doesn't exist yet, write a header
        with open(cornu_places, "r", encoding="utf8") as json_file:
            cornu_features = json.load(json_file)
            for n in txt_graph.nodes():
                tmp = mf.find_match_node(match_func, cornu_features, n, cornu_matched)
                if tmp != None:
                    found.append(n)
                    for t in tmp:
                        cornu_node = t[1]["properties"]["cornuData"]["cornu_URI"]
                        writer.writerow({"Geo Title": n,
                                         'Cornu Title': t[1]["properties"]["cornuData"]["toponym_arabic"],
                                         'Cornu Title Other': t[1]["properties"]["cornuData"]["toponym_arabic_other"],
                                         'lat': t[1]["properties"]["cornuData"]["coord_lat"],
                                         'lon': t[1]["properties"]["cornuData"]["coord_lon"],
                                         'Cornu Region': t[1]["properties"]["cornuData"]["region_code"],
                                         'Geo Neighbours': txt_graph[n],
                                         'Cornu Neighbours': cornu_graph[
                                             cornu_node] if cornu_node in cornu_graph else "null",
                                         'Cornu URI': cornu_node,
                                         'Status': match_status,
                                         'Match Method': method})
            return found


def get_pleiades_matches(place_names, pleiades_places, write_file):

    with open(pleiades_places, "r", encoding="utf8") as json_file:
        pleiades_features = json.load(json_file)
        with open(write_file, 'a', encoding="utf8") as matches_file:
            headers = ["Node", "Pleiades title", "Node Region", "Pleiades id", "Geometry", "Status", "Method"]
            writer = csv.DictWriter(matches_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
            writer.writeheader()  # write a header
            for p_name in place_names:
                n = p_name.split("-")[1].split("(")[0].strip()
                n_reg = p_name.split("-")[0].strip()
                # n_modern = p_name.split("-")[1].split("(")[1].translate(') ')
                for f in pleiades_features["@graph"]:
                    if len(f['features']) > 0:
                        if f['features'][0]['geometry'] != None:
                            if f['features'][0]['geometry']['type'] == "Point":
                                title = f['title']
                                # print("title: ",n, "-", title)
                                if n == title:
                                    # print("title true: ", n, "-", title)
                                    writer.writerow({'Node': n, 'Pleiades title': title,
                                                 "Node Region" : n_reg,
                                                 "Pleiades id": f['id'],
                                                 "Geometry": f['features'][0]['geometry']['coordinates'],
                                                 "Status": "NA", "Method": "Exact"})
                                    # continue
                                else:
                                    for name in f['names']:
                                        if n == name['id'] or n == name['attested'] or n == name['romanized']:
                                            writer.writerow({'Node': n, 'Pleiades title': title,
                                                             "Node Region" : n_reg,
                                                             "Pleiades id": f['id'], "Geometry": f['features'][0]['geometry']['coordinates'],
                                                             "Status": "NA", "Method": "Exact"})
                                            break

def get_trismegi_matches(graph, found_list , trismegi_places, write_file):
    # lemmatizer = LemmaReplacer('latin')
    with open(trismegi_places, "r", encoding="utf8") as trismegi_file:
        rows = pan.read_csv(trismegi_file, delimiter='\t')
        with open(write_file, 'a', encoding="utf8") as matches_file:
            headers = ["Node", "Trismegistos_Names", "Neighbours", "Status", "Method"]
            writer = csv.DictWriter(matches_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
            writer.writeheader()  # write a header
            for n in graph.nodes():
                if n not in found_list:
                # n_low = n.lower()
                # n_lemma = lemmatizer.lemmatize(n_low)
                # print(n_lemma)
                    for i, r in islice(rows.iterrows(), 1, None):
                        att_name = r['Attested Name']
                        language = r['Language']
                        tmp = r['TM Geo id'].split("-")
                        cano_name = tmp[1].strip() if len(tmp) > 1 else tmp[0].strip()
                        # if n in att_name or n in cano_name or n in language: # exact match
                        if mf.cosine_match(n, None, att_name, None): # string metrics
                            graph.node[n]['cano_name'].append(r['TM Geo id'])

                        elif mf.cosine_match(n, None, cano_name, None): # string metrics
                            graph.node[n]['cano_name'].append(r['TM Geo id'])

                        elif mf.cosine_match(n, None, language, None):  # string metrics
                            graph.node[n]['cano_name'].append(r['TM Geo id'])
                    if len(graph.node[n]['cano_name']) > 0:
                        writer.writerow({'Node': n, 'Trismegistos_Names': graph.node[n]['cano_name'],
                                         "Neighbours": graph.neighbors(n),
                                         "Status": "NA", "Method": "Cosine"})

    # with open(write_file, 'a', encoding="utf8") as matches_file:
    #     print("write!")
    #     headers = ["Node", "Trismegistos_Names", "Neighbours", "Status", "Method"]
    #     writer = csv.DictWriter(matches_file, delimiter='\t', quoting=csv.QUOTE_MINIMAL, fieldnames=headers)
    #     writer.writeheader()  # write a header
    #     for n in graph.nodes():
    #         tmp = graph.node[n]['cano_name']
    #         writer.writerow({'Node': n, 'Trismegistos_Names': tmp, "Neighbours": graph.neighbors(n),
    #                          "Status": "NA", "Method": "Smith"})



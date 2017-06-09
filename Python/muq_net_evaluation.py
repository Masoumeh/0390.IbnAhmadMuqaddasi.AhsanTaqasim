import networkx as nx
import json
import geograph.graph as ggraph
import geograph.map  as ggeo
import createGraphFromJSON_geoText_toJSON as cgjt


def net_eval(net_routes):
    G = cgjt.create_graph(net_routes)
    if not nx.is_connected(G):
        # get a list of unconnected networks
        sub_graphs = nx.connected_component_subgraphs(G)

        main_graph = sub_graphs[0]

        # find the largest network in that list
        for sg in sub_graphs:
            if len(sg.nodes())<100:
                print("sg nodes: ", sg.nodes())
            if len(sg.nodes()) < len(main_graph.nodes()):
                main_graph = sg
        print("nulls:")
        for n in G.nodes():
            if G.node[n]["lat"] == "null" and G.node[n]["lng"] == "null":
                print(G.node[n])
        # print("main: ",main_graph.nodes())


f1_muq = open("../Data/tripleRoutes_with_meter_basic_values", 'r')
json_routes = json.load(f1_muq)
net_eval(json_routes)

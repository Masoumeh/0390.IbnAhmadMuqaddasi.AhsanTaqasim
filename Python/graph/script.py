import create_graph as cg
import networkx as nx
import matplotlib.pyplot as plt
# g = cg.create_graph_csv("../../Data/Muqaddasi/muq_triples_route_wReg")
g = cg.create_graph_csv("/home/rostam/Desktop/Chiara/It.Ant. - tagged_new_it_tri")
# for n in g.nodes():
# g = cg.create_graph_geojson("../../Data/routes.json", "../../Data/places_new_structure.geojson")
print(len(g.nodes()))
# comp = sorted(nx.connected_components(g), key = len, reverse=False)
for n in g.nodes():
    print(n.split("_")[0], "\t", n.split("_")[1:], "\t", g.neighbors(n))



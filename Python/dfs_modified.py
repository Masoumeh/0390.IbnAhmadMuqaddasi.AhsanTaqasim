
import networkx as nx

G = nx.Graph()
G.add_path(['A','B'])
G.add_path(['A','C'])
G.add_path(['A','D'])
G.add_path(['B','E'])
G.add_path(['C','F'])
G.add_path(['D','G'])
G.add_path(['E','H'])
G.add_path(['E','I'])
G.add_path(['F','J'])
G.add_path(['G','K'])
G.add_path(['G','R'])
G.add_path(['J','L'])
G.add_path(['J','M'])
G.add_path(['J','N'])
G.add_path(['F','K'])
G.add_path(['K','O'])
G.add_path(['O','P'])
G.add_path(['O','Q'])
G.add_path(['O','S'])



# graph = {'A': set(['B', 'C']),
#          'B': set(['A', 'D', 'E']),
#          'C': set(['A', 'F']),
#          'D': set(['B']),
#          'E': set(['B', 'F']),
#          'F': set(['C', 'E'])}

T = nx.bfs_tree(G,'A')
print(T.edges())
print(list(nx.bfs_edges(G,'A')))
print(nx.bfs_successors(G,'A'))
# def dfs(start, deg):
#     # graph = g
#     visited, stack = set(), [start]
#     while stack:
#         vertex = stack.pop()
#         if vertex not in visited and graph.degree(vertex) <= deg:
#             visited.add(vertex)
#             stack.extend(graph[vertex] - visited)
#         elif graph.degree(vertex) > deg:
#             visited.add(vertex)
#             return visited
#     return visited


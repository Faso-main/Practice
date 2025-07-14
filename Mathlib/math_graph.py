import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_edges_from([(1, 2, {'weight': 4}), (2, 3, {'weight': 2}), (3, 4, {'weight': 3})])

pos = nx.spring_layout(G)

nx.draw(G, pos, with_labels=True)
edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()

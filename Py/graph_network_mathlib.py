import networkx as nx
import matplotlib.pyplot as plt

# Создаем граф
G = nx.Graph()

# Добавляем вершины и ребра
G.add_edges_from([('A', 'B'), ('A', 'C'), ('B', 'D'), ('B', 'E'), ('C', 'F'), ('E', 'F')])

# Визуализация
nx.draw(G, with_labels=True, node_color='lightblue', node_size=1000, font_size=12, font_weight='bold')
plt.title("Graph Visualization")
plt.show()

# Основные характеристики графа
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())
print("Degree of each node:", dict(G.degree()))
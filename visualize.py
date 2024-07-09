import networkx as nx
import matplotlib.pyplot as plt

def build_graph(edges):
    graph = {}
    for origem, destino, peso in edges:
        if origem not in graph:
            graph[origem] = {}
        graph[origem][destino] = peso
    return graph

def visualize_graph(graph):
    G = nx.DiGraph()
    for origem in graph:
        for destino in graph[origem]:
            G.add_edge(origem, destino, weight=graph[origem][destino])

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="lightblue", font_size=10, font_weight="bold", arrows=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

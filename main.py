from db import connect_to_db, get_graph_data
from algorithms import dijkstra, bellman_ford
from visualize import build_graph, visualize_graph

# Conectar ao banco de dados e obter dados do grafo
conn = connect_to_db('data/grafo.db')
edges = get_graph_data(conn)

# Construir o grafo e visualizar
graph = build_graph(edges)
visualize_graph(graph)

# Calcular o melhor caminho usando Dijkstra ou Bellman-Ford
start = 'A'  # Exemplo de ponto inicial
distances = dijkstra(graph, start)  # ou bellman_ford(graph, start)
print(distances)
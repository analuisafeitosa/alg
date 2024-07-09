import sqlite3

def connect_to_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn

def get_graph_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT origem, destino, peso FROM edges")
    return cursor.fetchall()

import pandas as pd
import networkx as nx
from scipy.io import mmread
import heapq

# 2. Carregar e Converter Arquivo `.mtx` para DataFrame
def carregar_e_converter_mtx(caminho_arquivo_mtx):
    # Carregar o arquivo .mtx usando scipy
    matrix = mmread(caminho_arquivo_mtx)

    # Converter a matriz carregada para um DataFrame do pandas
    grafo_df = pd.DataFrame(matrix.todense())

    # Renomear colunas para 'source', 'target' e 'weight' se necessário
    grafo_df.columns = ['source', 'target', 'weight']

    # Caso as colunas não estejam nomeadas corretamente ou existam colunas adicionais
    grafo_df = grafo_df.reset_index().rename(columns={0: 'source', 1: 'target', 2: 'weight'})

    # Garantir que as colunas tenham os tipos de dados corretos
    grafo_df['source'] = grafo_df['source'].astype(int)
    grafo_df['target'] = grafo_df['target'].astype(int)
    grafo_df['weight'] = grafo_df['weight'].astype(float)
    
    return grafo_df

# Caminho para o arquivo .mtx
caminho_arquivo_mtx = 'caminho_para_o_arquivo.mtx'
grafo_df = carregar_e_converter_mtx(caminho_arquivo_mtx)

# 3. Construir o Grafo com NetworkX
G = nx.Graph()

for _, row in grafo_df.iterrows():
    G.add_edge(row['source'], row['target'], weight=row['weight'])

# 4. Implementar o Algoritmo de Dijkstra
def dijkstra(G, start, end):
    queue = []
    heapq.heappush(queue, (0, start))
    distances = {node: float('infinity') for node in G.nodes}
    distances[start] = 0
    path = {node: None for node in G.nodes}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor in G.neighbors(current_node):
            weight = G[current_node][neighbor]['weight']
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
                path[neighbor] = current_node

    return distances, path

# 5. Reconstruir e Exibir o Caminho Mais Curto
def reconstruct_path(path, start, end):
    route = []
    current_node = end
    while current_node != start:
        route.append(current_node)
        current_node = path[current_node]
    route.append(start)
    route.reverse()
    return route

# Obter nós de início e destino do usuário
start_node = input('Digite o nó de início: ')
end_node = input('Digite o nó de destino: ')

# Encontrar o caminho mais curto
distances, path = dijkstra(G, start_node, end_node)
shortest_path = reconstruct_path(path, start_node, end_node)

print(f'O caminho mais curto de {start_node} a {end_node} é: {shortest_path}')

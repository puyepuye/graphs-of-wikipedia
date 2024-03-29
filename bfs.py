from collections import deque
import json
import os

def load_dict_from_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)
    else:
        return {}

def BFS_path(G, s1, s2):
    E = set([s2])
    Q = deque([[s1]])
    while Q:
        path = Q.popleft()
#         print(path)
        node = path[-1]
        if node not in G:
            raise ValueError
#         print(Q)
        if node == s2:
            return path
        if node not in E:
            adjacents = G[node]
            for i in adjacents:
                newpath = list(path)
                newpath.append(i)
                Q.append(newpath)
                E.add(node)
    return None


graph = load_dict_from_file('database/small_graph.json')
big_graph = load_dict_from_file('database/big_graph.json')
print(BFS_path(big_graph, 'University Of Toronto', 'Aurora College'))

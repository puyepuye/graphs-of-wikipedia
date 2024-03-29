from collections import deque
import json
import os

# on the go + visualization

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

def BFS_paths(G, s1, s2):
    """Find all paths from s1 to s2, only work with smaller graphs"""
    paths = []
    Q = deque([[s1]])
    while Q:
        path = Q.popleft()
        node = path[-1]
        if node == s2:
            paths.append(path)
        else:
            for neighbour in G.get(node, []):
                if neighbour not in path:
                    new_path = path + [neighbour]
                    Q.append(new_path)
    return paths

mini_graph = load_dict_from_file('database/mini_graph.json')
small_graph = load_dict_from_file('database/small_graph.json')
big_graph = load_dict_from_file('database/big_graph.json')
print(BFS_paths(mini_graph, 'Toronto Metropolitan University', 'Rhombicosidodecahedron'))

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

def BFS_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            new_paths = BFS_paths(graph, node, end, path)
            for new_path in new_paths:
                paths.append(new_path)
    return paths

def bfs_shortest_path_lengths(graph, source_item) -> dict:
    """
    Calculate the shortest path lengths from the source_item to all other vertices
    in the graph using a BFS traversal.

    Args:
    - graph: The graph object, instance of Graph.
    - source_item: The item stored in the source vertex.

    Returns:
    A dictionary mapping each vertex item to its shortest path length from the source.
    If a vertex is unreachable from the source, it will not appear in the dictionary.
    """
    # Initialize distances dictionary with infinity for all vertices
    distances = {vertex.item: float('inf') for vertex in graph._vertices.values()}
    # Set the distance to the source itself to 0
    distances[source_item] = 0

    # Queue for BFS, initialized with the source vertex
    queue = deque([source_item])

    while queue:
        current_item = queue.popleft()
        current_vertex = graph._vertices[current_item]

        for neighbour in current_vertex.neighbours:
            # If the neighbour hasn't been visited (distance is infinity)
            if distances[neighbour.item] == float('inf'):
                # Update the distance to this neighbour
                distances[neighbour.item] = distances[current_item] + 1
                # Add the neighbour to the queue for further exploration
                queue.append(neighbour.item)

    # Filter out the vertices that were not reachable (distance is still infinity)
    return {item: dist for item, dist in distances.items() if dist != float('inf')}

if __name__ == '__main__':
    mini_graph = load_dict_from_file('../database/mini_graph.json')
    small_graph = load_dict_from_file('../database/small_graph.json')
    big_graph = load_dict_from_file('../database/big_graph.json')
    print(BFS_paths(mini_graph, 'Toronto Metropolitan University', 'Rhombicosidodecahedron'))

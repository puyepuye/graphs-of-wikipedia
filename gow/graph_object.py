from __future__ import annotations
from visualize_helper import *
from collections import defaultdict
from typing import Any
from collections import deque
import json
import os
import wikipediaapi

class _Vertex:
    """A vertex in a graph.

    Instance Attributes:
        - item: The data stored in this vertex.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: Any
    neighbours: set[_Vertex]

    def __init__(self, item: Any, neighbours: set[_Vertex]) -> None:
        """Initialize a new vertex with the given item and neighbours."""
        self.item = item
        self.neighbours = neighbours

class Graph:
    """A graph.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        self._vertices[item] = _Vertex(item, set())

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            # Add the new edge
            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            self.add_vertex(item1)
            # We didn't find an existing vertex for both items.
            raise ValueError


    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            it1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in it1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError



    def add_all_edges(self, edges: set[tuple[Any, Any]]) -> None:
        """Add all given edges to this graph.

        Each element of edges is a tuple (x, y), representing the edge {x, y}.
        If an object in a given edge isn't represented by a vertex in this graph,
        add a new vertex containing the object to this graph before adding the edge.
        We strongly encourage you to make use of the Graph methods defined above.

        This method should NOT raise any ValueErrors.

        Preconditions:
        - all(edge[0] != edge[1] for edge in edges)

        >>> example_graph = Graph()
        >>> example_edges = {(1, 2), (1, 3), (3, 4)}
        >>> example_graph.add_all_edges(example_edges)
        >>> example_graph.get_neighbours(1) == {2, 3}
        True
        >>> example_graph.get_neighbours(3) == {1, 4}
        True
        """
        for v0, v1 in edges:
            if v0 not in self._vertices:
                self.add_vertex(v0)
            if v1 not in self._vertices:
                self.add_vertex(v1)
            self.add_edge(v0, v1)

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'user', 'book'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def all_edge(self) -> set:
        """
        >>> example_graph = Graph()
        >>> example_graph.add_vertex(10)
        >>> example_graph.add_vertex(20)
        >>> example_graph.add_vertex(30)
        >>> example_graph.add_vertex(40)
        >>> example_graph.add_edge(10, 20)
        >>> example_graph.add_edge(20, 30)
        >>> example_graph.add_edge(30, 40)
        >>> example_graph.all_edge()
        """
        edge_set = set()
        visited = set()
        for u in self._vertices:
            for i in self._vertices[u].neighbours:
                if i.item not in visited:
                    edge_set.add((u, i.item))
                    visited.add(u)
        return edge_set

    def create_subgraph_from_paths(graph, paths):
        """Create a new Graph containing only the nodes and edges from the given paths."""
        dict_graph = defaultdict(list)
        for path in paths:
            for i in range(len(path) - 1):
                dict_graph[path[i]].append(path[i + 1])

        graph = Graph()
        for page in dict_graph:
            graph.add_vertex(page)

        for page in dict_graph:
            for i in range(len(dict_graph[page])):
                if not dict_graph[page][i] in graph._vertices:
                    graph.add_vertex(dict_graph[page][i])
                graph.add_edge(page, dict_graph[page][i])

        return graph

def load_gow(pages_file: str) -> Graph:
    graph = Graph()
    unique_pages = {}

    # Step 1: Add all vertices
    with open(pages_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            page_id, page_title = row['page_id'], row['page_title']
            unique_pages[page_id] = page_title
            graph.add_vertex(page_title)

    with open(pages_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            page_id = row['page_id']
            page_title = unique_pages[page_id]
            outgoing_links = ast.literal_eval(row['outgoing_links'])

            for other_id in outgoing_links:
                other_title = unique_pages.get(str(other_id))
                if other_title:  # Check if the other page is in the dataset
                    graph.add_edge(page_title, other_title)

    return graph


def load_dict_from_file(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)
    else:
        return {}

def load_gow_json(pages_file: str):
    graph = Graph()
    unique_pages = load_dict_from_file(pages_file)

    #add_vertex
    for page in unique_pages:
        graph.add_vertex(page)

    #add_edge
    for page in unique_pages:
        for i in range(len(unique_pages[page])):
            if not unique_pages[page][i] in graph._vertices:
                graph.add_vertex(unique_pages[page][i])
            graph.add_edge(page, unique_pages[page][i])

    return graph, unique_pages



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
    return []

def DFS_paths(graph, start, end, path=[]):
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

def bidirectional(graph, start_article, end_article, bound=None):
    def get_links(article, graph):
        return graph.get(article, [])

    def get_backlinks(article, graph):
        backlinks = []
        for article_name, links in graph.items():
            if article in links:
                backlinks.append(article_name)
        return backlinks

    def extend_path(path, link):
        new_path = list(path)
        new_path.append(link)
        return new_path

    def remove_middle_section(path):
        visited = set()
        new_path = []

        for vertex in path:
            if vertex not in visited:
                visited.add(vertex)
                new_path.append(vertex)
            else:
                # Found the second occurrence of the vertex, remove the middle section
                idx = new_path.index(vertex)
                new_path = new_path[:idx + 1]
                visited = set(new_path)

        return tuple(new_path)

    paths = set()
    list_a = [[start_article]]
    list_b = [[end_article]]

    if not get_links(start_article, graph) or not get_backlinks(end_article, graph):
        return {}
    while list_a and list_b and (bound is None or len(paths) < bound) and len(list_a) < len(graph) and len(list_b) < len(graph):
        new_paths = []
        for path_a in list_a:
            current_article = path_a[-1]
            for link in get_links(current_article, graph):
                if link == end_article:
                    paths.add(tuple(path_a[::-1] + [link]))
                if link in list_b[0]:
                    idx = list_b[0].index(link)
                    new_path_a = extend_path(path_a, link)
                    new_path_b = list_b[0][:idx]
                    new_paths.append(new_path_a + new_path_b[::-1])
                elif link not in path_a:
                    new_paths.append(extend_path(path_a, link))
        list_a = new_paths

        new_paths = []
        for path_b in list_b:
            current_article = path_b[-1]
            for link in get_backlinks(current_article, graph):
                if link == start_article:
                    paths.add(tuple([link] + path_b[::-1]))
                if link in list_a[0]:
                    idx = list_a[0].index(link)
                    new_path_b = extend_path(path_b, link)
                    new_path_a = list_a[0][:idx]
                    if new_path_b[-1] == start_article:
                        paths.add(tuple([link] + path_b[::-1]))
                    new_paths.append(new_path_a[::-1] + new_path_b)
                elif link not in path_b:
                    new_paths.append(extend_path(path_b, link))
        list_b = new_paths

        for path_a in list_a:
            for path_b in list_b:
                if path_a[-1] == path_b[-1]:
                    paths.add(tuple(path_a + path_b[::-1]))
                if path_a[-1] == end_article:
                    paths.add(tuple(path_a))
                if path_b[-1] == start_article:
                    paths.add(tuple(path_b))
    return {remove_middle_section(path) for path in paths}


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
    graph_dict = load_dict_from_file('../database/small_graph.json')
    # visualize_paths(graph, graph_dict, 'University Of Toronto', 'Geodesy')
    start_article = 'Jarrow'
    end_article = 'Tree Model'
    paths = bidirectional(graph_dict, start_article, end_article)
    print(paths)
    print(BFS_path(graph_dict, start_article, end_article))

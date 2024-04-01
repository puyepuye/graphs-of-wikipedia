""" Modified Graph class from CSC111 Course Notes and various pathfinder algorithms for
finding paths between two Wikipedia articles """
from __future__ import annotations
from collections import defaultdict, deque
from typing import Any
import json
import os


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
    """A Modified graph object obtained from CSC111 course.

    Representation Invariants:
        - all(item == self._vertices[item].item for item in self._vertices)
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self.vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.
        """
        self.vertices[item] = _Vertex(item, set())

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            v2 = self.vertices[item2]

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
        if item1 in self.vertices and item2 in self.vertices:
            it1 = self.vertices[item1]
            return any(v2.item == item2 for v2 in it1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self.vertices:
            v = self.vertices[item]
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
            if v0 not in self.vertices:
                self.add_vertex(v0)
            if v1 not in self.vertices:
                self.add_vertex(v1)
            self.add_edge(v0, v1)

    def all_edge(self) -> set:
        """
        return a set of all edges in the graph
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
        for u in self.vertices:
            for i in self.vertices[u].neighbours:
                if i.item not in visited:
                    edge_set.add((u, i.item))
                    visited.add(u)
        return edge_set


def create_subgraph_from_paths(all_paths: list[str]) -> Graph:
    """Create a new Graph containing only the nodes and edges from the given paths."""
    dict_graph = defaultdict(list)
    for path in all_paths:
        for i in range(len(path) - 1):
            dict_graph[path[i]].append(path[i + 1])

    graph = Graph()
    for page in dict_graph:
        graph.add_vertex(page)

    for page in dict_graph:
        for i in range(len(dict_graph[page])):
            if not dict_graph[page][i] in graph.vertices:
                graph.add_vertex(dict_graph[page][i])
            graph.add_edge(page, dict_graph[page][i])

    return graph


def load_dict_from_file(file_name: str) -> dict:
    """Return the graph dictionary from JSON file. Each page is a key and all the outgoing links are the values."""
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return json.load(file)
    else:
        return {}


def load_gow_json(pages_file: str) -> tuple[Graph, dict]:
    """Return the graph as a Graph object and a dictionary of unique pages"""
    graph = Graph()
    unique_pages = load_dict_from_file(pages_file)

    # add_vertex
    for page in unique_pages:
        graph.add_vertex(page)

    # add_edge
    for page in unique_pages:
        for i in range(len(unique_pages[page])):
            if not unique_pages[page][i] in graph.vertices:
                graph.add_vertex(unique_pages[page][i])
            graph.add_edge(page, unique_pages[page][i])

    return graph, unique_pages


def bfs_path(graph: dict, s1: str, s2: str) -> list[str]:
    """Find and return a single path between article s1 and article s2 in the graph G"""
    visited = set(s2)
    queue = deque([[s1]])
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node not in graph:
            raise ValueError
        if node == s2:
            return path
        if node not in visited:
            adjacents = graph[node]
            for i in adjacents:
                newpath = list(path)
                newpath.append(i)
                queue.append(newpath)
                visited.add(node)
    return []


def get_links(article: str, loc_graph: dict) -> list[str]:
    """Helper function to return all outgoing links from the input article"""
    return loc_graph.get(article, [])


def get_backlinks(article: str, loc_graph: dict) -> list[str]:
    """Helper function to return all incoming links from the input article"""
    backlinks = []
    for article_name, links in loc_graph.items():
        if article in links:
            backlinks.append(article_name)
    return backlinks


def extend_path(path: list, loc_link: str) -> list[str]:
    """Helper function to return new extended path"""
    new_path = list(path)
    new_path.append(loc_link)
    return new_path


def remove_middle_section(path: list[str]) -> tuple[list[str]]:
    """Return a tuple of the paths deleting vertices that appears twice in the list."""
    visited = set()
    new_path = []

    for vertex in path:
        if vertex not in visited:
            visited.add(vertex)
            new_path.append(vertex)
        else:
            # Found the second occurrence of the vertex, remove the middle section
            ind = new_path.index(vertex)
            new_path = new_path[:ind + 1]
            visited = set(new_path)

    return tuple(new_path)


def find_intersection(paths: set, l_a: list, l_b: list, end: str, start: str) -> None:
    """Helper function to find intersection from the path from the start article and path from the end article."""
    for path_a in l_a:
        for path_b in l_b:
            if path_a[-1] == path_b[-1]:
                paths.add(tuple(path_a + path_b[::-1]))
            if path_a[-1] == end:
                paths.add(tuple(path_a))
            if path_b[-1] == start:
                paths.add(tuple(path_b))


def bidirectional(graph: dict, start: str, end: str, bound: int or bool = None) -> list:
    """ Pathfinder algorithm that start searches from the start and the end article simultaneosly and find the
    mid-point using incoming and outgoing links of each page. Return the list of shortest path with the size
    according to the input bound (number of paths)."""

    def append_new_paths_a() -> None:
        """Helper function to check intersecting links and append to paths (a)"""
        if link == end:
            paths.add(tuple(path_a[::-1] + [link]))
        if link in list_b[0]:
            idx = list_b[0].index(link)
            new_path_a = extend_path(path_a, link)
            new_path_b = list_b[0][:idx]
            new_paths.append(new_path_a + new_path_b[::-1])
        elif link not in path_a:
            new_paths.append(extend_path(path_a, link))

    def append_new_paths_b() -> None:
        """Helper function to check intersecting links and append to paths (b)"""
        if link == start:
            paths.add(tuple([link] + path_b[::-1]))
        if link in list_a[0]:
            idx = list_a[0].index(link)
            new_path_b = extend_path(path_b, link)
            new_path_a = list_a[0][:idx]
            if new_path_b[-1] == start:
                paths.add(tuple([link] + path_b[::-1]))
            new_paths.append(new_path_a[::-1] + new_path_b)
        elif link not in path_b:
            new_paths.append(extend_path(path_b, link))

    paths = set()
    list_a = [[start]]
    list_b = [[end]]

    if not get_links(start, graph) or not get_backlinks(end, graph):
        return []
    while list_a and list_b and (bound is None or len(paths) < bound) and len(list_a) < len(graph) and len(
            list_b) < len(graph):
        new_paths = []
        for path_a in list_a:
            current_article = path_a[-1]
            for link in get_links(current_article, graph):
                append_new_paths_a()
        list_a = new_paths

        new_paths = []
        for path_b in list_b:
            current_article = path_b[-1]
            for link in get_backlinks(current_article, graph):
                append_new_paths_b()
        list_b = new_paths
        find_intersection(paths, list_a, list_b, end, start)

    return sorted(list({remove_middle_section(path) for path in paths}), key=len)[:bound]


def bfs_shortest_path_lengths(graph: Graph, source_item: str) -> dict:
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
    distances = {vertex.item: float('inf') for vertex in graph.vertices.values()}
    # Set the distance to the source itself to 0
    distances[source_item] = 0

    # Queue for BFS, initialized with the source vertex
    queue = deque([source_item])

    while queue:
        current_item = queue.popleft()
        current_vertex = graph.vertices[current_item]

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
    # graph_dict = load_dict_from_file('../database/small_graph.json')
    # start_article = 'Jarrow'
    # end_article = 'Tree Model'
    # test_paths = bidirectional(graph_dict, start_article, end_article)
    # print(test_paths)
    # print(bfs_path(graph_dict, start_article, end_article))
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136', 'W0221', 'E9998'],
        'extra-imports': ['__future__', 'visualize_helper', 'networkx', 'collections', 'typing', 'json', 'os'],
        'max-nested-blocks': 4
    })


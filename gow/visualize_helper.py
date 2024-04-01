"""
This is a helper file that helps with visualizing.
Woohoo! Sorry, there's nothing more interesting to write here.
"""
from typing import Any
from plotly.graph_objs import Scatter, Figure
import networkx as nx
from graph_object import Graph, bfs_path, bidirectional, create_subgraph_from_paths, bfs_shortest_path_lengths


def edge_in_path(edge: str, path: list[str]) -> bool:
    """Check if an edge is in the shortest path."""
    return any(edge in {(path[i], path[i + 1]), (path[i + 1], path[i])} for i in range(len(path) - 1))


def convert_to_networkx(custom_graph: Graph) -> Graph:
    """Convert a custom graph object to a NetworkX graph."""
    nx_graph = nx.Graph()
    # Assuming your custom Graph has methods to access its vertices and edges
    for vertex in custom_graph.vertices:
        nx_graph.add_node(vertex)
    for edge in custom_graph.all_edge():
        # Assuming get_edges() returns a list of tuples (source, target)
        nx_graph.add_edge(edge[0], edge[1])
    return nx_graph


def summary(graph: dict, s1: Any, s2: Any, all_paths: list) -> dict[str, str]:
    """
    Returns a ductionary of information used for the main pygame app after graph has been visualized
    """
    min_len = len(bfs_path(graph, s1, s2))
    num_paths_min_len = len([i for i in all_paths if len(i) == min_len])
    summary_dict = {
        'min_path_len': f"The shortest path length between {s1} and {s2} is {min_len - 1}.",
        'num_of_paths': f"There are {len(all_paths)} possible path(s) between {s1} and {s2}.",
        'all_num_of_paths': f"There are more than {len(all_paths)} possible path(s) between {s1} and {s2}.",
        'num_of_paths_with_min_length': f"There are {num_paths_min_len} path(s) with the length {min_len - 1}.",
        'num_of_vertices': f"There are {len({point for path in all_paths for point in path})} vertices in this graph.",

    }
    return summary_dict


def visualize_paths(graph: Graph, graph_dict: dict, page_id1: str, page_id2: str, bound: int = None) -> list:
    """
    Visualize all paths between two vertices in a graph using networkx and plotly.
    """

    local_dict = {
        'all_paths': bidirectional(graph_dict, page_id1, page_id2, bound),
        'shortest_path': bfs_path(graph_dict, page_id1, page_id2),
        'path_lengths': bfs_shortest_path_lengths(graph, page_id1),
        'base_color': ['#ff0000', '#ff7f00', '#ffff00', '#7fff00', '#00ff00', '#0000ff'],
        'destination_color': '#000000',
        'node_color_mapping': {}
    }

    local_dict['subgraph'] = create_subgraph_from_paths(local_dict['all_paths'])
    local_dict['nx_subgraph'] = convert_to_networkx(local_dict['subgraph'])
    pos = nx.spring_layout(local_dict['nx_subgraph'])

    local_dict['x_values'], _ = zip(*pos.values())
    local_dict['min_x'], local_dict['max_x'] = min(local_dict['x_values']), max(local_dict['x_values'])

    # Set the start and end nodes at the extreme sides of the layout

    # Slightly left from the minimum x value
    pos[page_id1] = (local_dict['min_x'] - 0.1 * (local_dict['max_x'] - local_dict['min_x']), 0)
    # Slightly right from the maximum x value
    pos[page_id2] = (local_dict['max_x'] + 0.1 * (local_dict['max_x'] - local_dict['min_x']), 0)

    local_dict['max_distance'] = max(local_dict['path_lengths'].values(), default=0)
    local_dict['color_step'] = max(1, (len(local_dict['base_color']) - 1) / (local_dict['max_distance'] or 1))

    for node, distance in local_dict['path_lengths'].items():
        if node == page_id2:  # Apply special color to the destination node
            local_dict['node_color_mapping'][node] = local_dict['destination_color']
        else:
            local_dict['color_index'] = int(distance * local_dict['color_step']) % len(local_dict['base_color'])
            local_dict['node_color_mapping'][node] = local_dict['base_color'][local_dict['color_index']]

    # Nodes
    local_dict['node_x'] = []
    local_dict['node_y'] = []
    local_dict['text'] = []
    local_dict['node_colors'] = []  # List to hold colors for each node

    for node in local_dict['nx_subgraph'].nodes():
        local_dict['x'], local_dict['y'] = pos[node]
        local_dict['node_x'].append(local_dict['x'])
        local_dict['node_y'].append(local_dict['y'])
        local_dict['text'].append(str(node))
        # Fetch color from mapping, default to a fallback color if not found
        local_dict['node_colors'].append(local_dict['node_color_mapping'].get(node, "#000000"))

    # Now, create the node_trace with the correct colors for each node
    local_dict['node_trace'] = Scatter(
        x=local_dict['node_x'], y=local_dict['node_y'], text=local_dict['text'], mode='markers+text', hoverinfo='text',
        marker={"color": local_dict['node_colors'], "size": 10, "line": {"width": 2}}
    )

    # Separate lists for shortest path edges and other edges
    local_dict['shortest_edge_x'], local_dict['shortest_edge_y'] = [], []
    local_dict['other_edge_x'], local_dict['other_edge_y'] = [], []

    for edge in local_dict['nx_subgraph'].edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        if edge_in_path(edge, local_dict['shortest_path']):
            local_dict['shortest_edge_x'].extend([x0, x1, None])
            local_dict['shortest_edge_y'].extend([y0, y1, None])
        else:
            local_dict['other_edge_x'].extend([x0, x1, None])
            local_dict['other_edge_y'].extend([y0, y1, None])

    local_dict['shortest_path_trace'] = Scatter(
        x=local_dict['shortest_edge_x'], y=local_dict['shortest_edge_y'],
        line={"width": 2.5, "color": 'black'},
        hoverinfo='text',
        text='Shortest Path',
        mode='lines'
    )

    local_dict['other_edges_trace'] = Scatter(
        x=local_dict['other_edge_x'], y=local_dict['other_edge_y'],
        line={"width": 0.5, "color": '#888'},  # Regular edges
        hoverinfo='none',
        mode='lines'
    )

    fig = Figure(data=[local_dict['other_edges_trace'], local_dict['shortest_path_trace'], local_dict['node_trace']])
    fig.update_layout(
        showlegend=False,
        hovermode='closest',
        xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
        yaxis={"showgrid": False, "zeroline": False, "showticklabels": False}
    )

    fig.show()

    return local_dict['all_paths']


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136', 'W0221', 'E1101', 'E9998'],
        'extra-imports': ['networkx', 'graph_object', 'plotly.graph_objs '],
        'max-nested-blocks': 6
    })

import networkx as nx
from graph_object import *
from plotly.graph_objs import Scatter, Figure

def convert_to_networkx(custom_graph):
    """Convert a custom graph object to a NetworkX graph."""
    nx_graph = nx.Graph()
    # Assuming your custom Graph has methods to access its vertices and edges
    for vertex in custom_graph._vertices:
        nx_graph.add_node(vertex)
    for edge in custom_graph.all_edge():
        # Assuming get_edges() returns a list of tuples (source, target)
        nx_graph.add_edge(edge[0], edge[1])
    return nx_graph

def visualize_paths(graph: Graph, page_id1: str, page_id2: str) -> None:
    """
    Visualize all paths between two vertices in a graph using networkx and plotly.

    Args:
    - graph: The graph object (as a networkx Graph).
    - page_id1, page_id2: The IDs of the two vertices to find paths between.
    """

    # Find all paths between page_id1 and page_id2
    graph = convert_to_networkx(graph)
    print("hello")
    all_paths = list(nx.all_simple_paths(graph, source=page_id1, target=page_id2))

    # Create a subgraph that contains only the vertices and edges in these paths
    subgraph_nodes = set().union(*all_paths)  # Unpack all paths and get unique vertices
    subgraph = graph.subgraph(subgraph_nodes)

    pos = nx.spring_layout(subgraph)  # Position nodes using Fruchterman-Reingold force-directed algorithm

    # Edge trace
    edge_x = []
    edge_y = []
    for edge in subgraph.edges():
        print(edge)
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])  # None to interrupt the line
        edge_y.extend([y0, y1, None])

    edge_trace = Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')

    # Node trace
    node_x = []
    node_y = []
    text = []
    for node in subgraph.nodes():
        print(node)
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        text.append(str(node))

    node_trace = Scatter(x=node_x, y=node_y, text=text, mode='markers+text', hoverinfo='text', marker=dict(showscale=False, color='blue', size=10, line_width=2))
    fig = Figure(data=[edge_trace, node_trace])

    # Setting the layout directly without using 'go'
    fig.update_layout(
        showlegend=False,
        hovermode='closest',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )

    fig.show()  # Display


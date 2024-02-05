import pydotplus

def render_tree(root,regex):
    graph = create_graph(root)
    graph.write_png(f'result/{regex}.png')
    graph.write_svg(f'result/{regex}.svg')

def add_edges(graph, node, parent_id=None):
    if node is not None:
        node_id = str(id(node))
        graph.add_node(pydotplus.Node(node_id, label=str(node), shape='circle'))
        if parent_id is not None:
            graph.add_edge(pydotplus.Edge(parent_id, node_id))
        add_edges(graph, node.left, node_id)
        add_edges(graph, node.right, node_id)

def create_graph(root):
    graph = pydotplus.Dot(graph_type='graph')
    add_edges(graph, root)
    return graph
import pydotplus


def render_tree(root):
    graph = create_graph(root)
    graph.write_png("result/tree.png")
    graph.write_svg("result/tree.svg")


def add_edges(graph, node, parent_id=None):
    if node is not None:
        node_id = str(id(node))
        graph.add_node(pydotplus.Node(node_id, label=str(node), shape="circle"))
        if parent_id is not None:
            graph.add_edge(pydotplus.Edge(parent_id, node_id))
        add_edges(graph, node.left, node_id)
        add_edges(graph, node.right, node_id)


def create_graph(root):
    graph = pydotplus.Dot(graph_type="graph")
    add_edges(graph, root)
    return graph


def render_nfa(nfa):
    graph = pydotplus.Dot(graph_type="digraph")
    graph.set_rankdir("LR")
    added_states = set()
    graph.set_prog("neato")

    def add_states(state):
        if state.id in added_states:
            return
        added_states.add(state.id)
        graph.add_node(
            pydotplus.Node(
                str(state.id),
                shape="doublecircle" if state == nfa.final_state else "circle",
            )
        )
        for transition in state.transitions:
            graph.add_edge(
                pydotplus.Edge(
                    str(state.id),
                    str(transition.new_state.id),
                    label=str(transition.input),
                )
            )
            add_states(transition.new_state)

    add_states(nfa.initial_state)

    graph.write_png("result/nfa.png")
    graph.write_svg("result/nfa.svg")


def render_dfa(dfa):
    graph = pydotplus.Dot(graph_type="digraph")
    graph.set_rankdir("LR")
    graph.set_prog("neato")

    seen_states = set()

    for dfa_state in dfa.states:
        if dfa_state.id not in seen_states:
            graph.add_node(
                pydotplus.Node(
                    str(dfa_state.id),
                    shape="doublecircle" if dfa_state.is_accepting else "circle",
                )
            )
            seen_states.add(dfa_state.id)

        for input, new_dfa_state in dfa_state.transitions.items():
            if new_dfa_state.id not in seen_states:
                graph.add_node(
                    pydotplus.Node(
                        str(new_dfa_state.id),
                        shape="doublecircle"
                        if new_dfa_state.is_accepting
                        else "circle",
                    )
                )
                seen_states.add(new_dfa_state.id)

            graph.add_edge(
                pydotplus.Edge(
                    str(dfa_state.id),
                    str(new_dfa_state.id),
                    label=str(input),
                )
            )

    graph.write_png("result/dfa.png")
    graph.write_svg("result/dfa.svg")

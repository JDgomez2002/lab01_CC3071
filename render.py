import pydotplus

def render_tree(root,regex):
    graph = create_graph(root)
    graph.write_png(f'result/expression.png')
    graph.write_svg(f'result/expression.svg')

def add_edges(graph, node, parent_id=None):
    if node is not None:
        node_id = str(id(node))
        graph.add_node(pydotplus.Node(node_id, label=str(node).replace('set()','{Ø}'), shape='circle'))
        if parent_id is not None:
            graph.add_edge(pydotplus.Edge(parent_id, node_id))
        add_edges(graph, node.left, node_id)
        add_edges(graph, node.right, node_id)

def create_graph(root):
    graph = pydotplus.Dot(graph_type='graph')
    add_edges(graph, root)
    return graph

def create_dfa_graph(states, acceptance_states, transitions, symbols, start_state):
    # Convert sets to strings
    states = [str(state) for state in states]
    start_state = str(start_state)
    acceptance_states = [str(state) for state in acceptance_states]

    # Create a DOT format representation of the DFA
    dot = pydotplus.Dot()
    dot.set_rankdir("LR")  # Use 'TB' for top to bottom layout
    dot.set_prog("neato")

    # Create nodes for each state
    state_nodes = {}
    num = 0
    for state in states:
        node = pydotplus.Node(num)
        if state == start_state:
            node.set_name("Start")
            node.set_shape("circle")
            node.set_style("filled")

        if state in acceptance_states:
            node.set_shape("doublecircle")  # Final states are double circled
        node.set_fontsize(12)  # Set font size
        node.set_width(0.6)  # Set the desired width
        node.set_height(0.6)  # Set the desired height
        state_nodes[state] = node
        dot.add_node(node)

        num += 1

    # Add transitions as edges
    for (source, symbol, target) in transitions:
        edge = pydotplus.Edge(state_nodes[str(source)], state_nodes[str(target)], label=symbol)
        dot.add_edge(edge)

    return dot

def write_info_to_file(states, final_states, transitions, symbols, start_state, file_path):
    with open(file_path, 'w') as file:
        file.write("Estados = " + str(states) + "\n")
        file.write("Aceptacion = " + str(final_states) + "\n")
        file.write("Transicion = " + str(transitions) + "\n")
        file.write("Simbolos = " + str(symbols) + "\n")
        file.write("Inicio = " + str(start_state) + "\n")

def exec(estados, simbolos, estados_inicial, estados_aceptacion, transiciones):
    symbols = simbolos
    start_state = estados_inicial

    dfa_states, acceptance_states, dfa_transitions, start_state = dfa_to_nfa(
        estados,
        symbols,
        start_state,
        estados_aceptacion,
        transiciones,
    )

    # Remove entries with an empty set from dfa_states
    dfa_states = [state for state in dfa_states if state]

    # Remove entries with an empty set from acceptance_states
    acceptance_states = [state for state in acceptance_states if state]

    # Remove entries with an empty set from dfa_transitions
    dfa_transitions = [(state1, symbol, state2) for state1, symbol, state2 in dfa_transitions if state1 and state2]

    states = dfa_states
    final_states = acceptance_states
    transitions = dfa_transitions

    # Write information to a text file
    write_info_to_file(states, final_states, transitions, symbols, start_state, "texts/dfa_info.txt")

    pydotplus.find_graphviz()

    graph = create_dfa_graph(states, final_states, transitions, symbols, start_state)

    # Save or display the graph
    png_file_path = "pngs/dfa_graph.png"
    graph.write_png(png_file_path)  # Save PNG file

    return states, symbols, transitions, start_state, final_states


def create_direct_dfa_graph(states, transitions):
    # Convert sets to strings
    # states = [str(state) for state in states]
    # start_state = str(start_state)
    # acceptance_states = [state for state in acceptance_states]

    # Create a DOT format representation of the DFA
    dot = pydotplus.Dot()
    dot.set_rankdir("LR")  # Use 'TB' for top to bottom layout
    dot.set_prog("neato")

    # Create nodes for each state
    state_nodes = {}
    num = 0
    for state in states:
        if state.state != {'Ø'}:
            node = pydotplus.Node(num)
            node.set_name(str(state.state))
            if state.initial:
                # node.set_name("Start")
                node.set_shape("circle")
                node.set_style("filled")

            if state.accepting:
                node.set_shape("doublecircle")  # Final states are double circled
            node.set_fontsize(12)  # Set font size
            node.set_width(0.6)  # Set the desired width
            node.set_height(0.6)  # Set the desired height
            state_nodes[str(state.state)] = node
            # print(state.state)
            dot.add_node(node)

            num += 1

    for transition in transitions:
        if transition.symbol != '#':
            edge = pydotplus.Edge(state_nodes[str(transition.originState)], state_nodes[str(transition.destinationState)], label=str(transition.symbol))
            dot.add_edge(edge)

    pydotplus.find_graphviz()

    graph = dot

    # Save or display the graph
    png_file_path = "result/direct_dfa.png"
    graph.write_png(png_file_path)  # Save PNG file

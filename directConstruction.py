from syntax_tree import *
from render import create_direct_dfa_graph

class DirectDFAState:
    def __init__(self, state, marked=False, accepting=False, initial=False):
        self.state = state
        self.accepting = accepting
        self.marked = marked
        self.initial = initial

class DirectDFATransition:
    def __init__(self, symbol, originState, destinationState):
        self.symbol = symbol
        self.originState = originState
        self.destinationState = destinationState

class DirectDFA:
    def __init__(self, regex):
        self.states, self.transitions, self.alphabet = self.directConstruction(regex)

    def directConstruction(self, regex):
        if regex[-1] != '#':
            regex += '#' # add # to the end of the regex
        Dstates = []
        Dtransitions = []
        tree = SyntaxTree(regex)
        language = tree.operands
        node_map = tree.render()
        Dstates.append(DirectDFAState(calc_firstpos(tree.root), False, False, True)) # store root first pos

        nodeValueAndFollowpos = []
        for k, v in node_map.items(): # store node id, value, and followpos for every leaf node
            nodeSet = v.followpos
            if nodeSet == set():
                nodeSet = {'Ø'}
            nodeValueAndFollowpos.append([k, v.value, nodeSet])

        statesCounter = 0
        currentState = Dstates[statesCounter] # set current state to the first state in Dstates before entering while

        while ( any(not state.marked for state in Dstates) ): # if are any unmarked (False) state in Dstates
            currentState.marked = True # mark current state as marked (True)
            for symbol in language: # for every symbol in the operands of the regex
                newState = set() # create a new set for the new state
                for node in currentState.state: # for every follow pos in the current state
                    if isinstance(node, int): # if the node is a digit
                        if symbol == nodeValueAndFollowpos[node-1][1]: # if the symbol matches the value of the node
                            newState = newState.union(nodeValueAndFollowpos[node-1][2]) # add the follow pos of the node to the new state
                    else:
                        newState = {'Ø'} # if the node is not a digit, set the new state to empty
                if not newState == set(): # if the new state is not empty
                    currentStates = [] # create a new list for just the current states sets
                    for state in Dstates: # for every state in Dstates
                        currentStates.append(state.state) # add each state set() to the list to have all states and do a easy .contains() method check
                    # if len(currentStates) > 0:
                    if (newState is not None) and not (newState in currentStates): # if the new state is not in the list of current states
                        acceptingState = False
                        for endNode in newState:
                            if isinstance(endNode, int):
                                if nodeValueAndFollowpos[endNode-1][2] == {'Ø'}:
                                    acceptingState = True
                                    break
                        Dstates.append(DirectDFAState(newState, False, acceptingState)) # add the new state to Dstates
                    if currentState.state != {'Ø'}: # if the current state is not empty
                        Dtransitions.append(DirectDFATransition(symbol, currentState.state, newState)) # add the transition to Dtransitions
            statesCounter += 1 # increment the counter
            if (statesCounter < len(Dstates)):
                currentState = Dstates[statesCounter]
        
        return Dstates, Dtransitions, language
    
    def render(self):
        create_direct_dfa_graph(self.states, self.transitions)

    def run(self, string):
        # Verify if the string has chars that are not in the alphabet
        for char in string:
            if char not in self.alphabet:
                print(f'Direct DFA simulation with {string}: {False}')
                return False
        if string[-1] != '#':
            string += '#'
        currentState = self.states[0]
        for char in string:
            for transition in self.transitions:
                # print(currentState.state,transition.originState,transition.symbol,'-',char,transition.destinationState)
                if set(transition.originState) == set(currentState.state) and transition.symbol == char and char != '#':
                    for state in self.states:
                        if state.state == transition.destinationState:
                            currentState = state
                            # print('\tEureka!', char, currentState.state)
                            break
                    break
        # for transition in self.transitions:
        #     print(transition.symbol, transition.originState, transition.destinationState)
        # for state in self.states:
        #     print(state.state, state.accepting)
        if currentState.accepting:
            print(f'Direct DFA simulation with {string}: {True}')
            return True
        else: 
            print(f'Direct DFA simulation with {string}: {False}')
            return False

from typing import List, Dict
from nfa import State


class DFAState:
    id = 0

    def __init__(self, nfa_states: set[State]):
        self.nfa_states = nfa_states
        self.transitions: Dict[str, "DFAState"] = {}
        self.is_accepting = False
        self.id = DFAState.id
        DFAState.id += 1

    def __str__(self):
        nfa_state_ids = [str(nfa_state.id) for nfa_state in self.nfa_states]
        transitions = ", ".join(
            f"{input} -> {state.id}" for input, state in self.transitions.items()
        )
        return f"DFAState(id={self.id}, is_accepting={self.is_accepting}, nfa_states={nfa_state_ids}, transitions={transitions})"


class DFA:
    def __init__(self, initial_state: DFAState, states: List[DFAState]):
        self.initial_state = initial_state
        self.final_state = [state for state in states if state.is_accepting][0]
        self.states = states

from typing import List, Dict
from nfa import State


class DFAState:
    def __init__(self, nfa_states: set[State]):
        self.nfa_states = nfa_states
        self.transitions: Dict[str, "DFAState"] = {}
        self.is_accepting = any(
            state.is_accepting for state in nfa_states
        )  # Assuming State has an is_accepting attribute


class DFA:
    def __init__(self, initial_state: DFAState, states: List[DFAState]):
        self.initial_state = initial_state
        self.states = states

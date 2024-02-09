from typing import List


class Transition:
    def __init__(self, input, new_state):
        self.input = input
        self.new_state = new_state


class State:
    count = 0

    def __init__(self, transitions: List[Transition] = None):
        self.transitions = []
        self.id = State.count
        State.count += 1

        if transitions:
            self.transitions = transitions

    def add_transition(self, transition: Transition):
        self.transitions.append(transition)


class NFA:
    def __init__(self, initial_state: State, final_state: State):
        self.initial_state = initial_state
        self.final_state = final_state
        self.states = self.get_all_states(initial_state)

    def get_all_states(
        self, initial_state: State, visited: set[State] = None
    ) -> set[State]:
        if visited is None:
            visited = set()
        visited.add(initial_state)
        for transition in initial_state.transitions:
            if transition.new_state not in visited:
                self.get_all_states(transition.new_state, visited)
        return visited

    def input_symbols(self):
        return set(
            transition.input
            for state in self.states
            for transition in state.transitions
        )

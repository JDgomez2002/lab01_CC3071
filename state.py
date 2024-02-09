from typing import List


class Transition:
    def __init__(self, input: str, state):
        self.input = input
        self.state = state


class State:
    instance = 0

    def __init__(self, transitions: List[Transition] = None):
        self.transitions = []
        self.symbol = self.instance
        self.instance += 1
        if transitions:
            self.transitions = transitions

    def add_transition(self, transition: Transition):
        self.transitions.append(transition)

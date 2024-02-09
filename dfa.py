from typing import List, Dict
from nfa import State


class DFAState:
    id = 0

    def __init__(self, nfa_states: set[State]):
        self.nfa_states = nfa_states
        self.transitions: Dict[str, "DFAState"] = {}
        self.is_accepting = False
        self.id = DFAState.id
        self.is_start = False
        DFAState.id += 1

    def __str__(self):
        nfa_state_ids = [str(nfa_state.id) for nfa_state in self.nfa_states]
        transitions = ", ".join(
            f"{input} -> {state.id}" for input, state in self.transitions.items()
        )
        return f"DFAState(id={self.id}, is_accepting={self.is_accepting}, is_start={self.is_start}, nfa_states={nfa_state_ids}, transitions={transitions})"


class DFA:
    def __init__(self, initial_state: DFAState, states: List[DFAState]):
        self.initial_state = initial_state
        accepting_states = [state for state in states if state.is_accepting]
        self.final_state = accepting_states[0] if accepting_states else None
        self.states = states

    def input_symbols(self):
        return set(
            transition for state in self.states for transition in state.transitions
        )

    def remove_dead_states(self):
        reachable = set()

        def can_reach_accepting(state, visited=set()):
            if state in reachable:
                return True
            if state in visited:
                return False
            visited.add(state)

            for symbol, next_state in state.transitions.items():
                if next_state.is_accepting or can_reach_accepting(next_state, visited):
                    reachable.add(state)
                    return True
            return False

        # Check reachability from each non-accepting state
        for state in self.states:
            if not state.is_accepting:
                can_reach_accepting(state)

        # Filter out states that cannot reach an accepting state (i.e., dead states)
        self.states = [
            state for state in self.states if state in reachable or state.is_accepting
        ]

        # Update transitions to remove references to removed states
        for state in self.states:
            state.transitions = {
                symbol: next_state
                for symbol, next_state in state.transitions.items()
                if next_state in self.states
            }

    def printme(self):
        for state in self.states:
            for symbol, transition in state.transitions.items():
                print((state.id, transition.id, symbol))

        for state in self.states:
            print(state)

    def run(self, input_string: str):
        state = self.initial_state
        print(
            "Accepting states:",
            [state.id for state in self.states if state.is_accepting],
        )
        for symbol in input_string:
            print(
                "Reading:",
                symbol,
            )
            if symbol not in state.transitions:
                return "Rejected"

            print(
                "Current state:",
                state.id,
                "Next state:",
                state.transitions[symbol].id,
                "Symbol:",
                symbol,
            )
            state = state.transitions[symbol]

        if state.is_accepting:
            return "Accepted"

        return "Rejected"

    def minimize(self):
        # Step 1: Initial partitioning into accepting and non-accepting states
        partitions = {
            frozenset(state for state in self.states if state.is_accepting),
            frozenset(state for state in self.states if not state.is_accepting),
        }

        # Function to find the partition containing a specific state
        def find_partition(state, partitions):
            for partition in partitions:
                if state in partition:
                    return partition
            return None

        # Step 2: Refinement of partitions
        refined = True
        while refined:
            new_partitions = set()
            refined = False
            for partition in partitions:
                # Group states by where their transitions lead for each input symbol
                partition_mapping = {}
                for state in partition:
                    transition_signature = tuple(
                        find_partition(state.transitions.get(symbol), partitions)
                        for symbol in self.input_symbols()
                    )
                    if transition_signature not in partition_mapping:
                        partition_mapping[transition_signature] = set()
                    partition_mapping[transition_signature].add(state)

                if len(partition_mapping) > 1:  # Partition can be refined
                    refined = True
                    new_partitions.update(
                        frozenset(group) for group in partition_mapping.values()
                    )
                else:
                    new_partitions.add(partition)

            partitions = new_partitions

        # Step 3: Create new states for each partition and update transitions
        new_states = [DFAState(partition) for partition in partitions]
        # Update is_accepting for new states and create a mapping from old to new states
        old_to_new = {}
        for new_state in new_states:
            any_state = next(
                iter(new_state.nfa_states)
            )  # Any state from the partition to check if it was accepting
            new_state.is_accepting = any_state.is_accepting
            for old_state in new_state.nfa_states:
                old_to_new[old_state] = new_state

        # Update transitions for new states
        for new_state in new_states:
            for old_state in new_state.nfa_states:
                for symbol, state in old_state.transitions.items():
                    new_state.transitions[symbol] = old_to_new[state]

        # Identify the new initial and final states
        new_initial = old_to_new[self.initial_state]
        new_initial.is_start = True
        new_final_states = [state for state in new_states if state.is_accepting]

        # Update the DFA with the minimized information
        self.initial_state = new_initial
        self.states = new_states
        self.final_state = new_final_states[0] if new_final_states else None

        # self.remove_dead_states()

        # print transitions as tuples (from, to, symbol)
        # print("minimized uwu")

        # self.printme()

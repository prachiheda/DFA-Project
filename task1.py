import json
from collections import deque

class DFA:
    def __init__(self, states, alphabet, start_state, accept_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        # transitions[state][symbol] -> next_state
        self.transitions = transitions

def parse_dfa_json(dfa_json_str):
    """
    Given a JSON string describing a DFA, parse it into
    a DFA object.
    """
    data = json.loads(dfa_json_str)
    states = data["states"]
    alphabet = data["alphabet"]
    start_state = data["start_state"]
    accept_states = data["accept_states"]
    transitions = data["transitions"]
    
    return DFA(
        states=states,
        alphabet=alphabet,
        start_state=start_state,
        accept_states=accept_states,
        transitions=transitions
    )


def intersect_dfa(dfa1: DFA, dfa2: DFA) -> DFA:
    """
    Construct a new DFA that is the intersection of two given DFAs.
    The result will have tuple-states (s1, s2).
    """
    # We assume the DFAs share the same alphabet
    new_states = []
    new_transitions = {}
    new_accept_states = []
    
    for s1 in dfa1.states:
        for s2 in dfa2.states:
            new_states.append((s1, s2))

    # Build the transition function for the intersection
    for (s1, s2) in new_states:
        # For each tuple-state, we create a sub-dictionary for the transitions
        new_transitions[(s1, s2)] = {}
        for symbol in dfa1.alphabet:
            next_s1 = dfa1.transitions[s1][symbol]
            next_s2 = dfa2.transitions[s2][symbol]
            new_transitions[(s1, s2)][symbol] = (next_s1, next_s2)
    
    # Accept states in the intersection:
    # pairs (s1, s2) where s1 in dfa1.accept_states AND s2 in dfa2.accept_states
    for (s1, s2) in new_states:
        if s1 in dfa1.accept_states and s2 in dfa2.accept_states:
            new_accept_states.append((s1, s2))
    
    # Start state is just the tuple of start states
    new_start_state = (dfa1.start_state, dfa2.start_state)
    
    return DFA(
        states=new_states,
        alphabet=dfa1.alphabet,  
        start_state=new_start_state,
        accept_states=new_accept_states,
        transitions=new_transitions
    )


def is_language_empty(dfa: DFA) -> bool:
    """
    Return True if the DFA's language is empty, else False. Use a BFS style approach. 
    """
    
    visited = set()
    queue = deque()
    
    start = dfa.start_state
    queue.append(start)
    visited.add(start)
    
    while queue:
        current_state = queue.popleft()
        
        # Check if current state is accepting
        if current_state in dfa.accept_states:
            # We found a path to an accept state => language is not empty
            return False
        
        # Otherwise, explore neighbors
        # For each symbol in the alphabet, see where we go
        for symbol in dfa.alphabet:
            next_state = dfa.transitions[current_state][symbol]
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
    
    # If we exhaust all reachable states without finding an accept state:
    return True


def check_consistency(dfa_json_str_1, dfa_json_str_2) -> bool:
    """
    Return True if the two regular properties (represented by DFAs in JSON strings)
    are consistent, or False otherwise.
    """
    # Parse the two DFAs
    dfa1 = parse_dfa_json(dfa_json_str_1)
    dfa2 = parse_dfa_json(dfa_json_str_2)
    
    # Build the intersection DFA
    dfa_intersection = intersect_dfa(dfa1, dfa2)
    
    # Check if the intersection's language is empty
    empty = is_language_empty(dfa_intersection)
    
    # If it's empty, then the two DFAs (properties) are inconsistent
    if empty:
        print("False\n")
        print("The two input DFAs are inconsistent.")
        return not empty
    else:
        print("True\n")
        print("The two input DFAs are consistent.")
        return not empty
    

if __name__ == "__main__":
    w0_json = """
    {
        "states": ["qstart","q0", "q1"],
        "alphabet": ["0","1"],
        "start_state": "qstart",
        "accept_states": ["q0"],
        "transitions": {
            "qstart": { "0": "q0", "1": "q1" },
            "q0": { "0": "q0", "1": "q0" },
            "q1": { "0": "q1", "1": "q1" }
        }
    }
    """
    
    w1_json = """
    {
        "states": ["rstart","r0", "r1"],
        "alphabet": ["0","1"],
        "start_state": "rstart",
        "accept_states": ["r1"],
        "transitions": {
            "rstart": { "0": "r0", "1": "r1" },
            "r0": { "0": "r0", "1": "r0" },
            "r1": { "0": "r1", "1": "r1" }
        }
    }
    """

    # Requires at least 1 zero and at least 1 one
    x0_json = """
        {
        "states": ["q0", "q1", "q2", "q3"],
        "alphabet": ["0", "1"],
        "start_state": "q0",
        "accept_states": ["q3"],
        "transitions": {
            "q0": { "0": "q1", "1": "q2" },
            "q1": { "0": "q1", "1": "q3" },
            "q2": { "0": "q3", "1": "q2" },
            "q3": { "0": "q3", "1": "q3" }
        }
        }
    """

    # Requires at least 1 one
    x1_json = """

        {
        "states": ["r0", "r1"],
        "alphabet": ["0", "1"],
        "start_state": "r0",
        "accept_states": ["r1"],
        "transitions": {
            "r0": { "0": "r0", "1": "r1" },
            "r1": { "0": "r1", "1": "r1" }
        }
        }

    """
    print("Checking w0 and w1....\n")
    is_consistent = check_consistency(w0_json, w1_json)
    print("Consistent?", is_consistent)

    # print("Checking x0 and x1....\n")
    # is_consistent = check_consistency(x0_json, x1_json)
    # print("Consistent?", is_consistent)
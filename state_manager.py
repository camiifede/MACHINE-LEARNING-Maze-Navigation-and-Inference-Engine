# History management (for step/back functionality)

import copy  # Used to create deep copies of data structures to preserve their state

# Save the current state of the search
def save_state(open_set, visited, current_node, parents, open_dict, found, final_path, history):
    # Append a deep copy of the current state to the history list
    history.append((
        copy.deepcopy(open_set),
        copy.deepcopy(visited),
        copy.deepcopy(current_node),
        copy.deepcopy(parents),
        copy.deepcopy(open_dict),
        found,
        copy.deepcopy(final_path),
    ))

# Load the previous state from history (for undo/back functionality)
def load_previous_state(history):
    if len(history) > 1:
        history.pop()  # Remove the most recent state to revert to the previous one
    return copy.deepcopy(history[-1])  # Return a copy of the last state in history

# Save the current state of the search (for bidirectional search)
def save_state_bidirectional(queue_start, queue_goal, visited_start, visited_goal, expanded_node, parents_start, parents_goal, found, final_path, history):
    # Append a deep copy of the current state to the history list
    history.append((
        copy.deepcopy(queue_start),
        copy.deepcopy(queue_goal),
        copy.deepcopy(visited_start),
        copy.deepcopy(visited_goal),
        copy.deepcopy(expanded_node),
        copy.deepcopy(parents_start),
        copy.deepcopy(parents_goal),
        found,
        copy.deepcopy(final_path)
    ))

# Load the previous state from history (for undo/back in bidirectional search)
def load_previous_state_bidirectional(history):
    if len(history) > 1:
        history.pop()  # Remove the most recent state to go back
    return copy.deepcopy(history[-1])  # Return the previous state

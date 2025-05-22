# A* search algorithm (Node, heuristic, step-by-step search)

import heapq  # For implementing the priority queue
from constants import moves  # Not used in this file but may be used externally
from maze import is_valid    # Not used here but possibly for more complex validation
from constants import ROWS, COLS  # Grid boundaries

# Get all valid neighbor positions (up, down, left, right)
def get_neighbors(position):
    row, col = position
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Cardinal directions
    neighbors = []

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < ROWS and 0 <= c < COLS:  # Ensure within bounds
            neighbors.append((r, c))

    return neighbors

# Node class used for A* search
class Node:
    def __init__(self, position, g, h, parent=None):
        self.position = position       # (row, col) position of the node
        self.g = g                     # Cost from start node to this node
        self.h = h                     # Heuristic cost estimate to goal
        self.f = g + h                 # Total cost (f = g + h)
        self.parent = parent           # Parent node in the path

    def __lt__(self, other):
        return self.f < other.f        # Comparison based on f for priority queue ordering

# Heuristic function using Manhattan distance
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Reconstruct path from goal to start by following parent pointers
def reconstruct_path(node):
    path = []
    while node:
        path.append(node.position)
        node = node.parent
    return path[::-1]  # Reverse to get path from start to goal

# Expand current node: explore neighbors, update frontier and parent mappings
def expand_node(current_node, open_set, visited, parents, open_dict, obstacles, goal):
    new_frontier = []
    neighbors = get_neighbors(current_node.position)

    for neighbor in neighbors:
        if neighbor in obstacles or neighbor in visited:
            continue  # Skip if already visited or an obstacle

        tentative_g = current_node.g + 1  # Assume uniform cost of 1 for each move

        # Check if this path to neighbor is better than any previous one
        if neighbor not in open_dict or tentative_g < open_dict[neighbor]:
            neighbor_node = Node(neighbor, tentative_g, heuristic(neighbor, goal), current_node)
            heapq.heappush(open_set, neighbor_node)     # Add to priority queue
            open_dict[neighbor] = tentative_g           # Record best known cost
            parents[neighbor] = current_node.position    # Record parent for path reconstruction
            new_frontier.append(neighbor)               # Track newly added frontier nodes

    visited.add(current_node.position)  # Mark current as visited
    return new_frontier

# Utility function to print a path in readable format
def print_path(label, path):
    print(f"{label}: [{' -> '.join(str(p) for p in path)}]")

# Utility function to print current frontier (open list)
def print_frontier(open_dict):
    print("Frontier:", list(open_dict.keys()))

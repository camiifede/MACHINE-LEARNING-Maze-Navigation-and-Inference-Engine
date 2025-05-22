# Maze generation, solvability checking

import random  # For random obstacle placement
from collections import deque  # For BFS queue
from constants import moves  # Directions used to navigate the maze

# Check if a position is within bounds and not an obstacle
def is_valid(pos, rows, cols, obstacles):
    r, c = pos
    return 0 <= r < rows and 0 <= c < cols and pos not in obstacles

# Generate a set of random obstacles that still allows a valid path from start to goal
def generate_random_obstacles(start, goal, rows, cols, num_obstacles):
    # Generate a list of all cells in the grid
    all_cells = [(r, c) for r in range(rows) for c in range(cols)]
    all_cells.remove(start)
    all_cells.remove(goal)

    while True:
        # Randomly sample obstacle positions
        obstacles = set(random.sample(all_cells, num_obstacles))
        # Only return obstacles if the resulting maze is solvable
        if is_solvable(start, goal, obstacles, rows, cols):
            return obstacles

# Check if there's a path from start to goal using BFS
def is_solvable(start, goal, obstacles, rows, cols):
    queue = deque([start])
    visited = {start}

    while queue:
        current = queue.popleft()

        if current == goal:
            return True  # Found a path to the goal

        # Explore all neighboring cells
        for move in moves:
            neighbor = (current[0] + move[0], current[1] + move[1])
            if (
                0 <= neighbor[0] < rows and
                0 <= neighbor[1] < cols and
                neighbor not in obstacles and
                neighbor not in visited
            ):
                visited.add(neighbor)
                queue.append(neighbor)

    return False  # No path found to the goal

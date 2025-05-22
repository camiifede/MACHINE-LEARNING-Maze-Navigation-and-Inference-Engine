import heapq
from constants import moves, ROWS, COLS


# Manhattan distance heuristic
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Bidirectional Greedy Search algorithm
def bidirectional_greedy(start, goal, obstacles):
    # Priority queues for Greedy expansion from start and goal
    queue_start = [(heuristic(start, goal), start)]
    queue_goal = [(heuristic(goal, start), goal)]

    # Visited sets to track explored nodes
    visited_start = {start}
    visited_goal = {goal}

    # Parent mappings for path reconstruction
    parents_start = {start: None}
    parents_goal = {goal: None}

    # Store heuristic costs (useful for visualization or metrics)
    h_start = {start: heuristic(start, goal)}
    h_goal = {goal: heuristic(goal, start)}

    # Continue as long as there are nodes to explore in both queues
    while queue_start and queue_goal:
        # Expand one node from the start side
        if queue_start:
            _, current = heapq.heappop(queue_start)
            for move in moves:
                neighbor = (current[0] + move[0], current[1] + move[1])
                if (0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and
                        neighbor not in obstacles and neighbor not in visited_start):
                    visited_start.add(neighbor)
                    parents_start[neighbor] = current
                    h = heuristic(neighbor, goal)
                    h_start[neighbor] = h
                    heapq.heappush(queue_start, (h, neighbor))

                    # If this neighbor has already been visited from the goal side, path is found
                    if neighbor in visited_goal:
                        return reconstruct_path(parents_start, parents_goal, neighbor)

        # Expand one node from the goal side
        if queue_goal:
            _, current = heapq.heappop(queue_goal)
            for move in moves:
                neighbor = (current[0] + move[0], current[1] + move[1])
                if (0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and
                        neighbor not in obstacles and neighbor not in visited_goal):
                    visited_goal.add(neighbor)
                    parents_goal[neighbor] = current
                    h = heuristic(neighbor, start)
                    h_goal[neighbor] = h
                    heapq.heappush(queue_goal, (h, neighbor))

                    # Check if both searches meet
                    if neighbor in visited_start:
                        return reconstruct_path(parents_start, parents_goal, neighbor)

    return []  # Return empty path if no connection found


# Reconstruct the final path by combining paths from both search directions
def reconstruct_path(parents_start, parents_goal, meet):
    path = []

    # Trace path from meeting point back to the start
    node = meet
    while node is not None:
        path.append(node)
        node = parents_start[node]
    path.reverse()  # Reverse to get path from start to meeting point

    # Trace path from meeting point to the goal
    node = parents_goal[meet]
    while node is not None:
        path.append(node)
        node = parents_goal[node]

    return path

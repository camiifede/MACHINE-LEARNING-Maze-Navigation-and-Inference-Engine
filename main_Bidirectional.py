import pygame
import sys
import heapq
# Import constants, helper functions, and external modules
from constants import ROWS, COLS, CELL_SIZE, WINDOW_HEIGHT, start, goal, NUM_OBSTACLES, DEFAULT_OBSTACLES, moves
from maze import generate_random_obstacles
from bidirectional_Greedy import heuristic, reconstruct_path
from visualisation import draw_grid_bidirectional, draw_buttons
from state_manager import save_state_bidirectional, load_previous_state_bidirectional

# Initialize all search-related data structures
def reset_all(obstacles):
    # Queues for both directions
    queue_start = [(heuristic(start, goal), start)]
    queue_goal = [(heuristic(goal, start), goal)]
    # Visited nodes and parent tracking for both directions
    visited_start = {start}
    visited_goal = {goal}
    parents_start = {start: None}
    parents_goal = {goal: None}
    # Heuristic values for nodes
    h_start = {start: heuristic(start, goal)}
    h_goal = {goal: heuristic(goal, start)}
    # Search result status
    found = False
    final_path = []
    expanded_node_start = None
    expanded_node_goal = None
    history = []  # History stack for undo
    expanded_start = set()
    expanded_goal = set()

    # Save the initial state
    save_state_bidirectional(queue_start, queue_goal, visited_start, visited_goal, None, parents_start, parents_goal, found, final_path, history)

    return (queue_start, queue_goal, visited_start, visited_goal, parents_start, parents_goal,
            h_start, h_goal, found, final_path, expanded_node_start, expanded_node_goal, history,
            expanded_start, expanded_goal)

# Perform one step of the bidirectional search
def step_bidirectional(queue_start, queue_goal, visited_start, visited_goal,
                       parents_start, parents_goal, h_start, h_goal,
                       obstacles, expanded_start, expanded_goal):

    expanded_node_start = None
    expanded_node_goal = None

    # Expand from start direction
    if queue_start:
        _, current = heapq.heappop(queue_start)
        expanded_node_start = current
        expanded_start.add(current)
        for move in moves:
            neighbor = (current[0] + move[0], current[1] + move[1])
            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and neighbor not in obstacles and neighbor not in visited_start:
                parents_start[neighbor] = current
                visited_start.add(neighbor)
                h = heuristic(neighbor, goal)
                h_start[neighbor] = h
                heapq.heappush(queue_start, (h, neighbor))
                if neighbor in visited_goal:
                    return True, neighbor, expanded_node_start, expanded_node_goal

    # Expand from goal direction
    if queue_goal:
        _, current = heapq.heappop(queue_goal)
        expanded_node_goal = current
        expanded_goal.add(current)
        for move in moves:
            neighbor = (current[0] + move[0], current[1] + move[1])
            if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and neighbor not in obstacles and neighbor not in visited_goal:
                parents_goal[neighbor] = current
                visited_goal.add(neighbor)
                h = heuristic(neighbor, start)
                h_goal[neighbor] = h
                heapq.heappush(queue_goal, (h, neighbor))
                if neighbor in visited_start:
                    return True, neighbor, expanded_node_start, expanded_node_goal

    return False, None, expanded_node_start, expanded_node_goal

# Main visualization loop
def main():
    pygame.init()
    screen = pygame.display.set_mode((COLS * CELL_SIZE, WINDOW_HEIGHT))
    pygame.display.set_caption("Bidirectional Greedy Search Visualization")
    clock = pygame.time.Clock()

    # Start with randomized obstacles
    obstacles = generate_random_obstacles(start, goal, ROWS, COLS, NUM_OBSTACLES)
    print("Obstacles:", obstacles)

    # Initialize search data structures
    (queue_start, queue_goal, visited_start, visited_goal, parents_start, parents_goal,
     h_start, h_goal, found, final_path, expanded_node_start, expanded_node_goal, history,
     expanded_start, expanded_goal) = reset_all(obstacles)

    running = True
    while running:
        screen.fill((220, 220, 220))  # Light grey background

        # Determine the partial path from both sides
        if found:
            start_path = []
            goal_path = []
        else:
            def build_partial_path(parents, node):
                path = []
                while node is not None:
                    path.append(node)
                    node = parents.get(node)
                path.reverse()
                return path

            start_path = build_partial_path(parents_start, expanded_node_start) if expanded_node_start else []
            goal_path = build_partial_path(parents_goal, expanded_node_goal) if expanded_node_goal else []

        costs_combined = {**h_start, **h_goal}  # Combine heuristics for display

        # Draw the updated grid and buttons
        draw_grid_bidirectional(screen, visited_start, visited_goal, start_path, goal_path,
                                final_path, {**parents_start, **parents_goal}, obstacles, costs_combined)
        step_rect, back_rect, rand_rect, def_rect = draw_buttons(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if step_rect.collidepoint(event.pos):
                    # Save current state before taking a step
                    if (queue_start or queue_goal) and not found:
                        save_state_bidirectional(queue_start, queue_goal, visited_start, visited_goal, None,
                                                 parents_start, parents_goal, found, final_path, history)
                        found, meet_point, expanded_node_start, expanded_node_goal = step_bidirectional(
                            queue_start, queue_goal, visited_start, visited_goal,
                            parents_start, parents_goal, h_start, h_goal,
                            obstacles, expanded_start, expanded_goal
                        )

                        print("\n--- Step Taken ---")
                        if expanded_node_start:
                            print(f"Expanded from Start side: {expanded_node_start}")
                        if expanded_node_goal:
                            print(f"Expanded from Goal side: {expanded_node_goal}")
                        print(f"Frontier (Start Queue): {[item[1] for item in queue_start]}")
                        print(f"Frontier (Goal Queue): {[item[1] for item in queue_goal]}")
                        print(f"Total nodes expanded so far: {len(expanded_start.union(expanded_goal))}")

                        # If path is found, reconstruct and print it
                        if found:
                            final_path = reconstruct_path(parents_start, parents_goal, meet_point)
                            print("\n--- Goal reached! ---")
                            print(f"Solution path: {final_path}")

                if back_rect.collidepoint(event.pos):
                    # Undo last step
                    if len(history) > 1:
                        (queue_start, queue_goal, visited_start, visited_goal, _,
                         parents_start, parents_goal, found, final_path) = load_previous_state_bidirectional(history)
                        h_start = {n: heuristic(n, goal) for n in parents_start}
                        h_goal = {n: heuristic(n, start) for n in parents_goal}
                        expanded_node_start, expanded_node_goal = None, None
                        print("\n--- Went back one step ---")

                if rand_rect.collidepoint(event.pos):
                    # Load new randomized maze
                    obstacles = generate_random_obstacles(start, goal, ROWS, COLS, NUM_OBSTACLES)
                    print("Randomized obstacles:", obstacles)
                    (queue_start, queue_goal, visited_start, visited_goal, parents_start, parents_goal,
                     h_start, h_goal, found, final_path, expanded_node_start, expanded_node_goal, history,
                     expanded_start, expanded_goal) = reset_all(obstacles)

                if def_rect.collidepoint(event.pos):
                    # Load default obstacle set
                    obstacles = set(DEFAULT_OBSTACLES)
                    print("Default maze loaded:", obstacles)
                    (queue_start, queue_goal, visited_start, visited_goal, parents_start, parents_goal,
                     h_start, h_goal, found, final_path, expanded_node_start, expanded_node_goal, history,
                     expanded_start, expanded_goal) = reset_all(obstacles)

        pygame.display.update()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

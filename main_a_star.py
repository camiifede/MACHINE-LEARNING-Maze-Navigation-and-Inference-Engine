# Main loop: setup, Pygame window, event handling

import pygame
import sys
import heapq

from constants import ROWS, COLS, CELL_SIZE, WINDOW_HEIGHT, start, goal, NUM_OBSTACLES, DEFAULT_OBSTACLES
from maze import generate_random_obstacles
from a_star import Node, heuristic, reconstruct_path, expand_node, print_path, print_frontier
from visualisation import draw_grid, draw_buttons, draw_candidate_arrows
from state_manager import save_state, load_previous_state


def reset_all(obstacles):
    # Initialize/reset all data structures for a new search session
    open_set = []  # priority queue for nodes to explore
    start_node = Node(start, 0, heuristic(start, goal))
    heapq.heappush(open_set, start_node)
    visited = set()  # set of visited nodes
    parents = {start: None}  # parent links for reconstructing path
    open_dict = {start: 0}  # dictionary for quick cost lookup
    found = False  # goal not found yet
    final_path = []  # solution path
    current_node = None  # node currently being expanded
    history = []  # history for backtracking
    save_state(open_set, visited, current_node, parents, open_dict, found, final_path, history)
    return open_set, visited, current_node, parents, open_dict, found, final_path, history


def main():
    pygame.init()
    # Set up Pygame screen
    screen = pygame.display.set_mode((COLS * CELL_SIZE, WINDOW_HEIGHT))
    pygame.display.set_caption("A* Algorithm Visualization")
    clock = pygame.time.Clock()

    # Create initial obstacles
    obstacles = generate_random_obstacles(start, goal, ROWS, COLS, NUM_OBSTACLES)
    print("Obstacles:", obstacles)

    # Initialize search structures
    open_set, visited, current_node, parents, open_dict, found, final_path, history = reset_all(obstacles)

    running = True
    while running:
        screen.fill((220, 220, 220))  # Background color

        # Decide which path to draw: current path or final path
        current_display_path = reconstruct_path(current_node) if current_node and not found else final_path

        draw_grid(screen, visited, current_display_path, parents, obstacles, open_dict)

        # Draw arrows to show available moves from current node
        if current_node and not found:
            draw_candidate_arrows(screen, current_node.position, visited, obstacles)

        # Draw control buttons
        step_rect, back_rect, rand_rect, def_rect = draw_buttons(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit loop on window close
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle Step button (advance one step)
                if step_rect.collidepoint(event.pos):
                    if open_set and not found:
                        save_state(open_set, visited, current_node, parents, open_dict, found, final_path, history)

                        # Pop the lowest-f-cost node from the open set
                        current_node = heapq.heappop(open_set)
                        open_dict.pop(current_node.position, None)
                        print(f"\nExpanding node: {current_node.position}")
                        print_frontier(open_dict)
                        print_path("Current path", reconstruct_path(current_node))
                        print(f"Total nodes expanded: {len(visited) + 1}")

                        # Check if goal reached
                        if current_node.position == goal:
                            final_path = reconstruct_path(current_node)
                            found = True
                            print("\n--- Goal reached! ---")
                            print_path("Solution path", final_path)
                            print(f"Total nodes expanded: {len(visited) + 1}")
                            print("Final frontier (open set):", list(open_dict.keys()))

                        # Expand the current node (add neighbors to open set)
                        if current_node.position not in visited:
                            new_frontier = expand_node(current_node, open_set, visited, parents, open_dict, obstacles,
                                                       goal)
                            print("New frontier nodes added:", new_frontier)

                # Handle Back button (undo last step)
                if back_rect.collidepoint(event.pos):
                    if len(history) > 1:
                        open_set, visited, current_node, parents, open_dict, found, final_path = load_previous_state(history)
                        print("\n--- Went back one step ---")
                        print_frontier(open_dict)
                        if current_node:
                            print_path("Current path", reconstruct_path(current_node))
                        else:
                            print_path("Current path", [])

                # Handle Randomize Maze button
                if rand_rect.collidepoint(event.pos):
                    obstacles = generate_random_obstacles(start, goal, ROWS, COLS, NUM_OBSTACLES)
                    print("Randomized obstacles:", obstacles)
                    open_set, visited, current_node, parents, open_dict, found, final_path, history = reset_all(obstacles)

                # Handle Default Maze button
                if def_rect.collidepoint(event.pos):
                    obstacles = set(DEFAULT_OBSTACLES)
                    print("Default maze loaded:", obstacles)
                    open_set, visited, current_node, parents, open_dict, found, final_path, history = reset_all(obstacles)

        # Refresh the screen
        pygame.display.update()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

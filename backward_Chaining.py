# backward_Chaining.py

import pygame
import sys
from constants import ROWS, COLS, CELL_SIZE, WINDOW_HEIGHT, start, goal, DEFAULT_OBSTACLES, moves, NUM_OBSTACLES
from visualisation import draw_grid_backward_chaining, draw_buttons
from maze import generate_random_obstacles

# Utility to convert a grid position into a logical fact string
def at_fact(pos):
    return f"At{pos}"

# Generate backward chaining rules based on the grid and obstacle layout
def generate_backward_rules(rows, cols, obstacles):
    rules = []
    for r in range(rows):
        for c in range(cols):
            if (r, c) in obstacles:
                continue
            current = (r, c)
            for dr, dc in moves:
                neighbor = (r + dr, c + dc)
                if (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and neighbor not in obstacles):
                    rules.append({
                        'conclusion': at_fact(current),
                        'premises': [at_fact(neighbor)]
                    })
    return rules

# Backward chaining inference engine
def backward_chain(goal_fact, facts, rules, trace=None, visited=None, path=None):
    if trace is None:
        trace = []
    if visited is None:
        visited = set()
    if path is None:
        path = []

    # Goal is already known
    if goal_fact in facts:
        trace.append(f"Fact already known: {goal_fact}")
        path.append(eval(goal_fact[2:]))  # Convert 'At(r, c)' string back to tuple
        return True, trace, path

    # Avoid infinite loops
    if goal_fact in visited:
        trace.append(f"Already attempted and failed: {goal_fact}")
        return False, trace, path

    visited.add(goal_fact)
    trace.append(f"Trying to prove: {goal_fact}")

    # Find all rules that conclude this goal
    applicable_rules = [r for r in rules if r['conclusion'] == goal_fact]
    if not applicable_rules:
        trace.append(f"No rules lead to: {goal_fact}")
        return False, trace, path

    # Try each rule
    for rule in applicable_rules:
        trace.append(f"Found rule: {rule['conclusion']} <- {rule['premises']}")
        temp_path = []
        all_premises_true = True

        # Recursively attempt to prove all premises
        for premise in rule['premises']:
            result, trace, temp_path = backward_chain(premise, facts, rules, trace, visited, temp_path)
            if not result:
                trace.append(f"Failed to prove: {premise}")
                all_premises_true = False
                break

        if all_premises_true:
            trace.append(f"Rule succeeded:{rule['premises']} <- {rule['conclusion']} ")
            facts.add(goal_fact)
            temp_path.append(eval(goal_fact[2:]))  # Add current goal to path
            return True, trace, temp_path

    trace.append(f"All rules failed for: {goal_fact}")
    return False, trace, path

# Setup and run the inference engine, then return the final path
def run_inference(obstacles):
    initial_facts = {at_fact(goal)}  # Start from the goal
    rules = generate_backward_rules(ROWS, COLS, obstacles)

    print("\nFull Inference Rules")
    for rule in rules:
        print(f"{rule['conclusion']} <- {', '.join(rule['premises'])}")

    goal_fact = at_fact(start)  # Try to prove we're at the start
    success, trace, path = backward_chain(goal_fact, initial_facts, rules)

    print("\n--- Trace ---")
    for step in trace:
        print(step)

    return path

# Pygame GUI to visualize backward chaining step-by-step
def main():
    print("Backward-Chaining Maze Solver")
    pygame.init()
    screen = pygame.display.set_mode((COLS * CELL_SIZE, WINDOW_HEIGHT))
    pygame.display.set_caption("Backward-Chaining Path Visualization")
    clock = pygame.time.Clock()

    current_obstacles = DEFAULT_OBSTACLES.copy()
    full_path = run_inference(current_obstacles)
    step_index = 1  # For stepping through the path
    rule_display_map = {}  # Visual mapping of applied rules

    running = True
    while running:
        screen.fill((220, 220, 220))
        current_path = full_path[:step_index]  # Current visible path

        draw_grid_backward_chaining(screen, set(), set(), [], [], current_path, {}, current_obstacles, rule_display_map)
        step_rect, back_rect, rand_rect, def_rect = draw_buttons(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if step_rect.collidepoint(event.pos):
                    if step_index < len(full_path):
                        if step_index > 0:
                            from_pos = full_path[step_index - 1]
                            to_pos = full_path[step_index]
                            rule_text = f"{at_fact(from_pos)} <- {at_fact(to_pos)}"
                            rule_display_map[to_pos] = [rule_text]
                        step_index += 1

                elif back_rect.collidepoint(event.pos):
                    if step_index > 1:
                        removed_pos = full_path[step_index - 1]
                        rule_display_map.pop(removed_pos, None)
                        step_index -= 1

                elif rand_rect.collidepoint(event.pos):
                    current_obstacles = generate_random_obstacles(start, goal, ROWS, COLS, NUM_OBSTACLES)
                    full_path = run_inference(current_obstacles)
                    step_index = 1
                    rule_display_map = {}
                    print("Randomized maze generated.")

                elif def_rect.collidepoint(event.pos):
                    current_obstacles = DEFAULT_OBSTACLES.copy()
                    full_path = run_inference(current_obstacles)
                    step_index = 1
                    rule_display_map = {}
                    print("Default maze loaded.")

        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

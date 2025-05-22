# Drawing grid, arrows, buttons

import pygame
import math
from constants import ROWS, COLS, CELL_SIZE, start, goal, moves

def draw_arrow(screen, from_cell, to_cell, color=(100, 100, 255)):
    fx, fy = from_cell[1] * CELL_SIZE + CELL_SIZE // 2, from_cell[0] * CELL_SIZE + CELL_SIZE // 2
    tx, ty = to_cell[1] * CELL_SIZE + CELL_SIZE // 2, to_cell[0] * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.line(screen, color, (fx, fy), (tx, ty), 4)
    angle = math.atan2(ty - fy, tx - fx)
    arrow_size = 14
    for delta in [-0.4, 0.4]:
        end_x = tx - arrow_size * math.cos(angle + delta)
        end_y = ty - arrow_size * math.sin(angle + delta)
        pygame.draw.line(screen, color, (tx, ty), (end_x, end_y), 4)

def draw_grid(screen, visited, path, parents, obstacles, open_dict):
    font = pygame.font.SysFont(None, 20)
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = (255, 255, 255)
            pos = (r, c)
            if pos in obstacles:
                color = (0, 0, 0)
            elif pos == start:
                color = (0, 255, 0)
            elif pos == goal:
                color = (255, 0, 0)
            elif pos in path:
                color = (0, 0, 255)
            elif pos in visited:
                color = (200, 200, 200)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

            #Show cost value if this cell is in the open set (frontier)
            if pos in open_dict:
                cost_text = font.render(str(open_dict[pos]), True, (0, 0, 0))
                screen.blit(cost_text, (c * CELL_SIZE + 4, r * CELL_SIZE + 4))

    for pos in visited:
        if pos == start or pos not in parents:
            continue
        parent = parents[pos]
        if parent is not None:
            draw_arrow(screen, parent, pos)


def draw_grid_bidirectional(screen, visited_start, visited_goal, start_path, goal_path, final_path, parents, obstacles, costs):
    font = pygame.font.SysFont(None, 20)
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = (255, 255, 255)  # Default white

            pos = (r, c)
            if pos in obstacles:
                color = (0, 0, 0)  # Black for walls
            elif pos == start:
                color = (0, 255, 0)  # Green for Start
            elif pos == goal:
                color = (255, 0, 0)  # Red for Goal
            elif pos in final_path:
                color = (0, 0, 255)  # Blue for Final Solution Path
            elif pos in start_path:
                color = (255, 255, 0)  # Yellow for Start Partial Path
            elif pos in goal_path:
                color = (255, 140, 0)  # Orange for Goal Partial Path
            elif pos in visited_start or pos in visited_goal:
                color = (200, 200, 200)  # Light grey for explored cells

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Grid lines

            if pos in costs:
                cost_text = font.render(str(costs[pos]), True, (0, 0, 0))
                screen.blit(cost_text, (c * CELL_SIZE + 4, r * CELL_SIZE + 4))
    # Draw arrows
    for pos in visited_start.union(visited_goal):
        if pos == start or pos == goal or pos not in parents:
            continue
        parent = parents[pos]
        if parent is not None:
            draw_arrow(screen, parent, pos)

def draw_grid_backward_chaining(screen, visited_start, visited_goal, start_path, goal_path, final_path, parents, obstacles, rule_map=None):
    font = pygame.font.SysFont(None, 14)
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = (255, 255, 255)
            pos = (r, c)

            if pos in obstacles:
                color = (0, 0, 0)
            elif pos == start:
                color = (0, 255, 0)
            elif pos == goal:
                color = (255, 0, 0)
            elif pos in final_path:
                color = (255, 255, 0)
            elif pos in start_path:
                color = (255, 255, 0)
            elif pos in goal_path:
                color = (255, 140, 0)
            elif pos in visited_start or pos in visited_goal:
                color = (200, 200, 200)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)

            if rule_map and pos in rule_map:
                for i, line in enumerate(rule_map[pos][:2]):
                    text = font.render(line, True, (50, 50, 50))
                    screen.blit(text, (c * CELL_SIZE + 2, r * CELL_SIZE + 2 + i * 14))



    # Draw arrows
    for pos in visited_start.union(visited_goal):
        if pos == start or pos == goal or pos not in parents:
            continue
        parent = parents[pos]
        if parent is not None:
            draw_arrow(screen, parent, pos)


def draw_candidate_arrows(screen, current_pos, visited, obstacles):
    from constants import ROWS, COLS, moves
    for move in moves:
        neighbor = (current_pos[0] + move[0], current_pos[1] + move[1])
        # Check if neighbor is within bounds
        if (0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS):
            if neighbor not in obstacles and neighbor not in visited:
                draw_arrow(screen, current_pos, neighbor, color=(255, 140, 0))


def draw_buttons(screen):
    font = pygame.font.SysFont(None, 24)
    top_y = ROWS * CELL_SIZE
    step_rect = pygame.Rect(0, top_y, 124, 35)
    back_rect = pygame.Rect(124, top_y, 124, 35)
    rand_rect = pygame.Rect(248, top_y, 124, 35)
    def_rect = pygame.Rect(372, top_y, 110, 35)

    pygame.draw.rect(screen, (0, 200, 0), step_rect)
    pygame.draw.rect(screen, (200, 0, 0), back_rect)
    pygame.draw.rect(screen, (0, 0, 200), rand_rect)
    pygame.draw.rect(screen, (0, 0, 0), def_rect)

    step_txt = font.render("Step", True, (255,255,255))
    back_txt = font.render("Back", True, (255,255,255))
    rand_txt = font.render("Randomize", True, (255,255,255))
    def_txt = font.render("Default Maze", True, (255,255,255))

    screen.blit(step_txt, (step_rect.centerx - step_txt.get_width()//2, step_rect.centery - step_txt.get_height()//2))
    screen.blit(back_txt, (back_rect.centerx - back_txt.get_width()//2, back_rect.centery - back_txt.get_height()//2))
    screen.blit(rand_txt, (rand_rect.centerx - rand_txt.get_width()//2, rand_rect.centery - rand_txt.get_height()//2))
    screen.blit(def_txt, (def_rect.centerx - def_txt.get_width()//2, def_rect.centery - def_txt.get_height()//2))

    pygame.display.flip()
    return step_rect, back_rect, rand_rect, def_rect

import sys
from math import sqrt

import pygame

import properties as pr
import grid as grid_module

camera_pos = (0, 0)
mouse_down_pos = (0, 0)

class Button(pygame.sprite.Sprite):
    def __init__(self, game_state, pos, text, action):
        super().__init__(game_state.button_sprites)
        self.game_state = game_state
        self.pos = pos
        self.action = action
        self.image = pygame.Surface((120, 30))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill(pr.DARK_GREEN_RGB)
        font = pygame.font.SysFont("Calibri", 24)
        self.text = font.render(text, True, pr.WHITE_RGB)
        self.image.blit(self.text, (5, 5))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.game_state.game_finished = True

def reset(menu, func):
    """Serves as a kind of decorator for functions connected with menu buttons,
    but it's not the real decorator because it takes dynamical menu argument as an input"""
    def new_func(*args, **kwargs):
        res = func(*args, **kwargs)
        menu.full_reset()
        print('Reset happened!')
        return res
    return new_func

def draw(screen, game_state):
    """Draws all game objects on given surface"""
    screen.fill(pr.BLACK_RGB)
    grid = game_state.grid
    grid_surface = grid.surface

    for h in grid.hexes():
        # grid_surface.blit(h.texture, h.vertices['top_left'])
        if h.grid_type == pr.GridType.PLAIN:
            pygame.draw.polygon(grid_surface, pr.WHITE_RGB, list(h.vertices.values()))
        else:
            grid_surface.blit(h.texture, h.hex_texture_corner_pos)
        if h.object is not None:
            grid_surface.blit(h.object.texture, h.object_texture_corner_pos)
        pygame.draw.aalines(grid_surface, pr.DARK_GREEN_RGB, True, list(h.vertices.values()))

    screen.blit(grid_surface, grid_surface.get_rect())
    game_state.button_sprites.draw(screen)


def handle_event(e):
    """Handles user events according to game logic"""
    # print(e.type, e)
    finished = False
    if e.type == pygame.MOUSEBUTTONDOWN:
        return handle_mouse_button_down(*e.pos), finished

    if e.type == pygame.MOUSEBUTTONUP:
        return handle_mouse_button_up(*e.pos), finished

    if e.type == pygame.QUIT or (hasattr(e, 'key') and e.key == pr.button_keys['esc']):
        finished = True

    return do_nothing, finished


def handle_mouse_button_down(x, y):
    """Handles event when user click on point (x, y) according to game logic"""
    def handler(_):
        global mouse_down_pos
        mouse_down_pos = (x, y)

    return handler


def handle_mouse_button_up(x, y):
    """Handles event when user releases mouse button on point (x, y) according to game logic"""
    def handler(grid):
        global camera_pos
        if mouse_down_pos == (x, y):
            el = grid.get_hex_edge_length()
            hex_pos = grid_module.pixel_to_hex(x - el - camera_pos[0],
                                        y - el * sqrt(3) / 2 - camera_pos[1], el)
            print(x, y, hex_pos)
            hex = grid.get_hex(*hex_pos)
            if hex is not None:
                hex.update_grid_type(pr.GridType.FOREST)
        else:
            diff_x, diff_y = x - mouse_down_pos[0], y - mouse_down_pos[1]
            camera_pos = (camera_pos[0] + diff_x, camera_pos[1] + diff_y)

    return handler


def do_nothing(_):
    """Handles event by doing nothing"""
    pass

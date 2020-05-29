"""
smg.py -- the game
==================
Core package describing top level game logic.
"""
import sys
from math import sqrt

import pygame

import grid
import properties

tick_milliseconds = 100
camera_pos = (0, 0)
mouse_down_pos = (0, 0)


def main():
    """Start game cycle"""
    pygame.init()
    draw_request_event_type = pygame.USEREVENT
    pygame.time.set_timer(draw_request_event_type, tick_milliseconds)
    screen = pygame.display.set_mode((properties.window_width, properties.window_height),
                                     pygame.RESIZABLE)
    world = grid.Grid(properties.grid_width, properties.grid_height, properties.hex_edge_length)
    surface = pygame.Surface(world.get_grid_resolution())

    while True:
        draw(surface, world)
        screen.blit(surface, camera_pos)

        event = pygame.event.wait()
        action = handle_event(event)
        action(world)
        if event.type == draw_request_event_type:
            pygame.display.flip()


def draw(surface, world):
    """Draws all game objects on given surface"""
    surface.fill((255, 255, 255))

    for h in world.hexes():
        # surface.blit(h.texture, h.vertices['top_left'])
        # pygame.draw.polygon(surface, h.color, h.vertices())
        surface.blit(h.texture, h.corner_pos)
        pygame.draw.aalines(surface, (98, 113, 113), True, list(h.vertices.values()))


def handle_event(e):
    """Handles user events according to game logic"""
    # print(e.type, e)
    if e.type == pygame.MOUSEBUTTONDOWN:
        return handle_mouse_button_down(*e.pos)

    if e.type == pygame.MOUSEBUTTONUP:
        return handle_mouse_button_up(*e.pos)

    if e.type == pygame.QUIT or (hasattr(e, 'key') and e.key == properties.button_keys['esc']):
        return finish

    return do_nothing


def handle_mouse_button_down(x, y):
    """Handles event when user click on point (x, y) according to game logic"""
    def handler(_):
        global mouse_down_pos
        mouse_down_pos = (x, y)

    return handler


def handle_mouse_button_up(x, y):
    """Handles event when user releases mouse button on point (x, y) according to game logic"""
    def handler(world):
        global camera_pos
        if mouse_down_pos == (x, y):
            el = world.get_hex_edge_length()
            hex_pos = grid.pixel_to_hex(x - el - camera_pos[0],
                                        y - el * sqrt(3) / 2 - camera_pos[1], el)
            print(x, y, hex_pos)
            # for h in world.hexes():
            #     h.color = (0, 0, 0)
            world.get_hex(*hex_pos).update_grid_type(properties.GridType.FOREST)
        else:
            diff_x, diff_y = x - mouse_down_pos[0], y - mouse_down_pos[1]
            camera_pos = (camera_pos[0] + diff_x, camera_pos[1] + diff_y)

    return handler


def do_nothing(_):
    """Handles event by doing nothing"""


def finish(_):
    """Handles event by exiting the game"""
    sys.exit(0)


if __name__ == '__main__':
    main()

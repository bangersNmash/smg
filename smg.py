import sys
from math import sqrt

import pygame

import grid
import properties

# todo: Consider making not global.
camera_pos = (0, 0)
mouse_down_pos = (0, 0)


def main():
    pygame.init()
    screen = pygame.display.set_mode((properties.window_width, properties.window_height),
                                     pygame.RESIZABLE)
    surface = pygame.Surface((properties.grid_width * properties.default_size * 2,
                              (properties.grid_height + 1) * properties.default_size * sqrt(3)))
    world = grid.Grid(properties.grid_width, properties.grid_height, properties.default_size)

    while True:
        screen.fill((255, 255, 255))

        draw(surface, world)

        screen.blit(surface, camera_pos)
        pygame.display.update()

        action = handle_event(pygame.event.wait())
        action(world)


def draw(surface, world):
    surface.fill((255, 255, 255))
    for h in world.hexes():
        pygame.draw.polygon(surface, h.color, h.vertices())
        pygame.draw.aalines(surface, (255, 255, 255), True, h.vertices())


def handle_event(e):
    if e.type == pygame.MOUSEBUTTONDOWN:
        return handle_mouse_button_down(*e.pos)

    if e.type == pygame.MOUSEBUTTONUP:
        return handle_mouse_button_up(*e.pos)

    if e.type == pygame.QUIT:
        return finish

    return do_nothing


def handle_mouse_button_down(x, y):
    def handler(_):
        global mouse_down_pos
        mouse_down_pos = (x, y)

    return handler


def handle_mouse_button_up(x, y):
    def handler(world):
        global camera_pos
        if mouse_down_pos == (x, y):
            size = world.get_size()
            hex_pos = grid.pixel_to_hex(x - size - camera_pos[0],
                                        y - size * sqrt(3) / 2 - camera_pos[1], size)
            print(x, y, hex_pos)

            for h in world.hexes():
                h.color = (0, 0, 0)
            world.get_hex(*hex_pos).color = (255, 0, 0)
        else:
            diff_x, diff_y = x - mouse_down_pos[0], y - mouse_down_pos[1]
            camera_pos = (camera_pos[0] + diff_x, camera_pos[1] + diff_y)

    return handler


def do_nothing(_):
    pass


def finish(_):
    sys.exit(0)


if __name__ == '__main__':
    main()

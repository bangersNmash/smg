import sys
from math import sqrt

import pygame

import grid
import properties


def main():
    pygame.init()
    screen = pygame.display.set_mode((properties.width, properties.height))
    map = grid.Grid(properties.width, properties.height, properties.default_size)

    while True:
        draw(screen, map)
        action = handle_event(pygame.event.wait())
        action(map)


def draw(screen, map):
    screen.fill((255, 255, 255))
    for hex in map.hexes():
        pygame.draw.aalines(screen, (0, 0, 0), True, hex.vertices())
    pygame.display.update()


def handle_event(e):
    if e.type == pygame.MOUSEBUTTONDOWN:
        return handle_click(*e.pos)

    if e.type == pygame.QUIT:
        return finish
    return id


def handle_click(x, y):
    def f(map):
        size = map.get_size()
        print(x, y, grid.pixel_to_hex(x - size, y - size * sqrt(3) / 2, properties.default_size))

    return f


def id(_):
    pass


def finish(_):
    sys.exit(0)


if __name__ == '__main__':
    main()

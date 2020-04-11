import sys
from math import sqrt

import pygame

import grid
import properties


def main():
    pygame.init()
    screen = pygame.display.set_mode((properties.width, properties.height), pygame.RESIZABLE)
    surface = screen.copy()
    map = grid.Grid(properties.width, properties.height, properties.default_size)

    while True:
        draw(surface, map)
        screen.blit(surface, (0, 0))
        pygame.display.update()

        action = handle_event(pygame.event.wait())
        action(map)


def draw(screen, world):
    screen.fill((255, 255, 255))
    for hex in world.hexes():
        pygame.draw.polygon(screen, hex.color, hex.vertices())
        pygame.draw.aalines(screen, (255, 255, 255), True, hex.vertices())


def handle_event(e):
    if e.type == pygame.MOUSEBUTTONDOWN:
        return handle_click(*e.pos)

    if e.type == pygame.QUIT:
        return finish
    return id


def handle_click(x, y):
    def f(world):
        size = world.get_size()
        hex_pos = grid.pixel_to_hex(x - size, y - size * sqrt(3) / 2, size)
        print(x, y, hex_pos)

        for hex in world.hexes():
            hex.color = (0, 0, 0)
        world.get_hex(*hex_pos).color = (255, 0, 0)

    return f


def id(_):
    pass


def finish(_):
    sys.exit(0)


if __name__ == '__main__':
    main()

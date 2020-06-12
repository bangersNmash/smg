"""
grid.py -- hexagonal grid
==========================
Provides data structures and operations representing grid of hexagons.
"""

from math import sqrt
import random
import pygame
from gui import frame_image

import properties as pr


class Hex:
    """Represents a hexagon"""

    def __init__(self, x, y,
                 size=pr.hex_edge_length,
                 hex_type=pr.HexType.PLAIN,
                 object=None):
        self.x, self.y = x, y
        self.size = size
        self.width, self.height = pr.hex_width, pr.hex_height
        self.update_hex_type(hex_type)

        self.object = object
        self.vertices = self.compute_vertices()
        self.hex_texture_corner_pos = (self.x - (self.width / 2), self.y - (self.height / 2))
        self.object_texture_corner_pos = (self.x - (self.width / 4), self.y - (self.height / 4))

    def update_hex_type(self, hex_type):
        self.hex_type = hex_type
        self.texture = pygame.image.load(pr.grid_type2img[self.hex_type])
        # self.texture = pygame.transform.rotate(self.texture, 60)
        self.texture = pygame.transform.scale(self.texture, (int(self.width), int(self.height)))

    def compute_vertices(self):
        """Returns list of hexagon's vertices from left one clockwise"""
        h = self.height
        w = self.width
        return {
            'left': (self.x - w / 2, self.y),
            'top_left': (self.x - w / 4, self.y - h / 2),
            'top_right': (self.x + w / 4, self.y - h / 2),
            'right': (self.x + w / 2, self.y),
            'bottom_right': (self.x + w / 4, self.y + h / 2),
            'bottom_left': (self.x - w / 4, self.y + h / 2)
        }


class Grid(pygame.sprite.Sprite):
    """Represents a grid of hexagons"""

    def __init__(self, sprite_group, bg_surface_data, width_in_hexes, height_in_hexes,
                 hex_edge_length=pr.hex_edge_length, objects=None):
        super().__init__(sprite_group)
        self.width_in_hexes, self.height_in_hexes = width_in_hexes, height_in_hexes
        self._hex_edge_length = hex_edge_length
        self._grid = []
        self.hex_width, self.hex_height = pr.hex_width, pr.hex_height
        self.width, self.hex = self.get_grid_resolution()
        self.objects = objects

        self.bg_surface, self.bg_surface_rect = bg_surface_data
        self.shift_x, self.shift_y = self.bg_surface_rect.topleft

        self.surface = pygame.Surface(self.get_grid_resolution())
        self.surface_rect = self.surface.get_rect(topleft=(0, 0))
        self.surface.fill(pr.WHITE_RGB)

        obj_with_positions = []
        for obj in objects:
            obj_with_positions.append((obj.grid_position, obj))
        obj_with_positions = sorted(obj_with_positions, key=lambda t: t[0])
        print(obj_with_positions)

        obj_i = 0
        y = i = 0
        while i < height_in_hexes:
            row = []
            x, j = 0, 0
            while j < width_in_hexes:
                x_coord = x + self.hex_width / 2
                y_coord = y + (j % 2 + 1) / 2 * self.hex_height
                gts = pr.HexType.type_names()
                gt_i = random.randrange(0, len(gts))

                if obj_i < len(obj_with_positions) and (i, j) == obj_with_positions[obj_i][0]:
                    row.append(Hex(x_coord, y_coord, hex_edge_length,
                                   hex_type=pr.HexType[gts[gt_i]],
                                   object=obj_with_positions[obj_i][1]))
                    print('Obj appended!')
                    obj_i += 1
                else:
                    row.append(Hex(x_coord, y_coord, hex_edge_length,
                                   hex_type=pr.HexType[gts[gt_i]],
                                   object=None))
                x += hex_edge_length * 1.5
                j += 1
            self._grid.append(row)
            y += self.hex_height
            i += 1

        self.observed_hex = None

    def get_hex(self, row, col):
        """Get hexagon at position (row, col)"""
        if row >= self.height_in_hexes or row < 0:
            return None
        if col >= self.width_in_hexes or col < 0:
            return None
        return self._grid[row][col]

    def get_hex_edge_length(self):
        """Get length of hexagon side"""
        return self._hex_edge_length

    def get_grid(self):
        """Get hexes as bi-dimensional grid"""
        return self._grid

    def hexes(self):
        """Get hexes as list from left to right, from top to bottom"""
        hexes = []
        for row in self._grid:
            for elem in row:
                hexes.append(elem)
        return hexes

    def get_grid_resolution(self):
        """Get grid resolution in pixels"""
        width = self.width_in_hexes * self.hex_width - pr.hex_edge_length / 2
        height = (pr.grid_height + 0.5) * pr.hex_height
        return width, height

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == pr.MouseButton.RIGHT:
            x, y = event.pos
            x, y = x - self.shift_x, y - self.shift_y
            el = self.get_hex_edge_length()
            hex_pos = pixel_to_hex(x - el,
                                   y - el * sqrt(3) / 2, el)
            hex = self.get_hex(*hex_pos)
            if hex is not None:
                print(x, y, hex_pos)
                self.observed_hex = hex
            else:
                self.observed_hex = None
        elif event.type == pygame.MOUSEMOTION and event.buttons[0] == pr.MouseButton.LEFT and \
                self.bg_surface_rect.collidepoint(event.pos):
            dx, dy = event.rel
            self.shift_x += dx
            self.shift_y += dy
            self.surface_rect.move_ip(dx, dy)
        else:
            pass

    def draw(self, screen):
        for h in self.hexes():
            self.surface.blit(h.texture, h.hex_texture_corner_pos)
            if h.object is not None:
                self.surface.blit(h.object.texture, h.object_texture_corner_pos)
            pygame.draw.lines(self.surface, pr.DARK_GREEN_RGB, True, list(h.vertices.values()))
        self.bg_surface.blit(self.surface, self.surface_rect)
        frame_image(self.bg_surface)
        screen.blit(self.bg_surface, self.bg_surface_rect)


def hex_to_pixel(row, col, hex_edge_length):
    """Get pixel on surface from position of a hexagon in a grid"""
    x = hex_edge_length * 3 / 2 * col
    y = hex_edge_length * sqrt(3) * (row + 0.5 * (col & 1))
    return x, y


def pixel_to_hex(x, y, hex_edge_length):
    """Get position of a hexagon in a grid from pixel on surface"""
    q, r = _axial_pixel_to_hex(x, y, hex_edge_length)
    cx, cy, cz = _axial_to_cube(q, r)
    col, row = _cube_to_normal(cx, cy, cz)
    return int(row), int(col)


def _cube_to_normal(x, _, z):
    """Translate cubic coordinates to square grid coordinates"""
    col = x
    row = z + (x - (x & 1)) / 2
    return col, row


def _axial_pixel_to_hex(x, y, size):
    """Translate pixel coordinates on axial surface to hex position on axial surface"""
    q = (2. / 3 * x) / size
    r = (-1. / 3 * x + sqrt(3) / 3 * y) / size
    return _axial_hex_round(q, r)


def _axial_hex_round(q, r):
    """Round axial coordinates to nearest"""
    return _cube_to_axial(*_cube_round(*_axial_to_cube(q, r)))


def _cube_round(x, y, z):
    """Round cube coordinates to nearest"""
    rx = round(x)
    ry = round(y)
    rz = round(z)

    x_diff = abs(rx - x)
    y_diff = abs(ry - y)
    z_diff = abs(rz - z)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry - rz
    elif y_diff > z_diff:
        ry = -rx - rz
    else:
        rz = -rx - ry

    return rx, ry, rz


def _cube_to_axial(x, _, z):
    """Convert from cubic (x, y, z) coordinates to axial (q, r) coordinates"""
    q = x
    r = z
    return q, r


def _axial_to_cube(q, r):
    """Convert from axial (q, r) coordinates to cubic (x, y, z) coordinates"""
    x = q
    z = r
    y = -x - z
    return x, y, z

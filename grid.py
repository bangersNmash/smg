"""
grid.py -- hexagonal grid
==========================
Provides data structures and operations representing grid of hexagons.
"""

from math import sqrt

import properties
import pygame


class Hex:
    """Represents a hexagon"""
    def __init__(self, x, y,
                 size=properties.hex_edge_length,
                 grid_type=properties.GridType.PLAIN,
                 object=None):
        self.x, self.y = x, y
        self.size = size
        self.width, self.height = properties.hex_width, properties.hex_height
        self.update_grid_type(grid_type)

        self.object = object
        self.vertices = self.compute_vertices()
        self.corner_pos = (self.x - (self.width / 2), self.y - (self.height / 2))

    def update_grid_type(self, grid_type):
        self.grid_type = grid_type
        self.texture = pygame.image.load(properties.grid_type2img[self.grid_type])
        # self.texture = pygame.transform.rotate(self.texture, 60)
        self.texture = pygame.transform.scale(self.texture, (int(self.width), int(self.height)))

    def compute_vertices(self):
        """Returns list of hexagon's vertices from left one clockwise"""
        h = self.height
        w = self.width
        return {
            'left': (self.x - w / 2, self.y),
            'top_left': (self.x - w / 4, self.y - h / 2),
            'top_right': (self.x +  w / 4, self.y - h / 2),
            'right': (self.x + w / 2, self.y),
            'bottom_right': (self.x + w / 4, self.y + h / 2),
            'bottom_left': (self.x - w / 4, self.y + h / 2)
        }


class Grid:
    """Represents a grid of hexagons"""
    def __init__(self, width, height, hex_edge_length=properties.hex_edge_length):
        self.width, self.height = width, height
        self._hex_edge_length = hex_edge_length
        self._grid = []
        self.hex_width, self.hex_height = properties.hex_width, properties.hex_height

        y = i = 0
        while i < height:
            row = []
            x, j = 0, 0
            while j < width:
                x_coord = x + self.hex_width / 2
                y_coord = y + (j % 2 + 1) / 2 * self.hex_height
                row.append(Hex(x_coord, y_coord, hex_edge_length))
                x += hex_edge_length * 1.5
                j += 1
            self._grid.append(row)
            y += self.hex_height
            i += 1

    def get_hex(self, row, col):
        """Get hexagon at position (row, col)"""
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
        width = self.width * self.hex_width - properties.hex_edge_length / 2
        height = (properties.grid_height + 0.5) * properties.hex_height
        return width, height

def hex_to_pixel(row, col, size):
    """Get pixel on surface from position of a hexagon in a grid"""
    x = size * 3 / 2 * col
    y = size * sqrt(3) * (row + 0.5 * (col & 1))
    return x, y


def pixel_to_hex(x, y, size):
    """Get position of a hexagon in a grid from pixel on surface"""
    q, r = _axial_pixel_to_hex(x, y, size)
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

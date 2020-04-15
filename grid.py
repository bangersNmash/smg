from math import sqrt

import properties


class Hex:
    def __init__(self, x, y, size, color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def vertices(self):
        h = self.size * sqrt(3)
        return [
            [self.x - self.size, self.y],  # left
            [self.x - self.size / 2, self.y - h / 2],  # top left
            [self.x + self.size / 2, self.y - h / 2],  # top right
            [self.x + self.size, self.y],  # right
            [self.x + self.size / 2, self.y + h / 2],  # bottom right
            [self.x - self.size / 2, self.y + h / 2],  # bottom left
        ]


class Grid:
    def __init__(self, width, height, size=properties.default_size):
        self._size = size
        self._grid = []

        hex_width, hex_height = size * 2, size * sqrt(3)

        y = i = 0
        while i < height:
            row = []
            x, j = 0, 0
            while j < width:
                row.append(Hex(x + hex_width / 2, y + (j % 2 + 1) / 2 * hex_height, size))
                x += size * 1.5
                j += 1
            self._grid.append(row)
            y += hex_height
            i += 1

    def get_hex(self, row, col):
        return self._grid[row][col]

    def get_size(self):
        return self._size

    def get_grid(self):
        return self._grid

    def hexes(self):
        hexes = []
        for row in self._grid:
            for elem in row:
                hexes.append(elem)
        return hexes


def hex_to_pixel(row, col, size):
    """Get pixel on surface from row and column of a hex"""
    x = size * 3 / 2 * col
    y = size * sqrt(3) * (row + 0.5 * (col & 1))
    return x, y


def pixel_to_hex(x, y, size):
    """Get row and column of a hex in grid from pixel on surface"""
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

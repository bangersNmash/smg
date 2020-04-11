from math import sqrt

import properties


class Hex:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

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
        while y < height:
            row = []
            x = (i % 2) * size * 1.5
            while x < width:
                row.append(Hex(x + hex_width / 2, y + hex_height / 2, size))
                x += hex_width * 1.5
            self._grid.append(row)
            y += hex_height / 2
            i += 1

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
    x = size * 3 / 2 * col
    y = size * sqrt(3) * (row + 0.5 * (col & 1))
    return x, y


def pixel_to_hex(x, y, size):
    q, r = _axial_pixel_to_hex(x, y, size)
    cx, cy, cz = _axial_to_cube(q, r)
    col, row = _cube_to_normal(cx, cy, cz)
    return row, col


def _cube_to_normal(x, y, z):
    col = x
    row = z + (x - (x & 1)) / 2
    return col, row


def _axial_pixel_to_hex(x, y, size):
    q = (2. / 3 * x) / size
    r = (-1. / 3 * x + sqrt(3) / 3 * y) / size
    return _axial_hex_round(q, r)


def _axial_hex_round(q, r):
    return _cube_to_axial(*_cube_round(*_axial_to_cube(q, r)))


def _cube_round(x, y, z):
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
    q = x
    r = z
    return q, r


def _axial_to_cube(q, r):
    x = q
    z = r
    y = -x - z
    return x, y, z

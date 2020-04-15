"""
test_grid.py -- test file for grid.py
"""
from math import sqrt

from grid import _cube_to_axial, pixel_to_hex, _axial_to_cube, _axial_hex_round, hex_to_pixel


def test_hex_to_pixel():
    """Tests grid.hex_to_pixel on fixed random hexes"""
    size = 10
    h = size * sqrt(3)

    x, y = hex_to_pixel(0, 0, size)
    assert x == 0 and y == 0

    x, y = hex_to_pixel(0, 1, size)
    assert x == size * 1.5 and y == h / 2

    x, y = hex_to_pixel(0, 2, size)
    assert x == size * 3 and y == 0


def test_pixel_to_hex():
    """Tests grid.pixel_to_hex on fixed random pixels"""
    size = 10  # px
    w = 2 * size

    row, col = pixel_to_hex(0, 0, size)
    assert row == 0 and col == 0

    row, col = pixel_to_hex(size, 0, size)
    assert row == 0 and col == 0

    row, col = pixel_to_hex(w + 1, size + 1, size)
    assert row == 0 and col == 1

    row, col = pixel_to_hex(w * 1.5 + 1, 0, size)
    assert row == 0 and col == 2

    # row, col = pixel_to_hex(w * 1.5 + 1, 2 * size, size)
    # assert row == 0 and col == 1


def test_cube_to_axial():
    """Tests grid._cube_to_axial on fixed random cube coordinates"""
    x, y, z = -2, 0, 2
    q, _ = _cube_to_axial(x, y, z)
    assert q == -2 and z == 2


def test_axial_to_cube():
    """Tests grid._axial_to_cube on fixed random axial coordinates"""
    q, r = -1, -1
    x, y, z = _axial_to_cube(q, r)
    assert x == -1 and y == 2 and z == -1


def test_hex_round():
    """Tests grid._axial_to_cube: conversion from axial to cube coordinates"""
    q, r = 0.6, -1.6
    qr, rr = _axial_hex_round(q, r)
    assert qr == 1 and rr == -2

    q, r = -0.9, -1.6
    qr, rr = _axial_hex_round(q, r)
    assert qr == -1 and rr == -2

    q, r = 0, -0.4
    qr, rr = _axial_hex_round(q, r)
    assert qr == 0 and rr == 0

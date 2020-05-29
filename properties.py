"""
properties.py -- external configuration
"""
from enum import Enum, auto
from math import sqrt
# Grid parameters
grid_width = 6  # hex
grid_height = 6  # hex
class GridType(Enum):
    HILL = 0
    WATER_OBJECT = 1
    FOREST = 2
    PLAIN = 3

grid_type2img = {
    GridType.HILL: './textures/blank_hex.png',
    GridType.WATER_OBJECT: './textures/blank_hex.png',
    GridType.FOREST: './textures/forest_hex.png',
    GridType.PLAIN: './textures/blank_hex.png'
}

# Hex parameters
hex_edge_length = 50  # px
hex_width = hex_edge_length * 2 # px
hex_height = hex_edge_length * sqrt(3) # px

# Window parameters
window_width = 600  # px
window_height = 600  # px


# Keyboard button keys defined inside pygame
button_keys = {
    'esc': 27,
}

# Server
db_name = "db/mydatabase.db"
default_players = 2
round_duration = 1 * 60

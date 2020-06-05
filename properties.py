"""
properties.py -- external configuration
"""
from enum import Enum, auto
from math import sqrt

# Grid parameters
grid_width = 5  # hex
grid_height = 5  # hex
class HexType(Enum):
    HILL = 0
    WATER_OBJECT = 1
    FOREST = 2
    PLAIN = 3

    def __str__(self):
        return f"{self.name} hex"

    @staticmethod
    def type_names():
        return ['HILL', 'WATER_OBJECT', 'FOREST', 'PLAIN']

grid_type2img = {
    HexType.HILL: './textures/hexes/hill.png',
    HexType.WATER_OBJECT: './textures/hexes/water.png',
    HexType.FOREST: './textures/hexes/forest.png',
    HexType.PLAIN: './textures/hexes/plain.png'
}

# Hex parameters
hex_edge_length = 40  # px
hex_width = hex_edge_length * 2 # px
hex_height = hex_edge_length * sqrt(3) # px

# Window parameters
game_window_width = 800  # px
game_window_height = 600  # px
menu_window_width = 800 # px
menu_window_height = 800 # px

# Character parameters
class CharacterType(Enum):
    WIZARD = 0
    TOUGH = 1
    ARCHER = 2
    @staticmethod
    def type_names():
        return ['WIZARD', 'TOUGH', 'ARCHER']

character_type2img= {
    CharacterType.WIZARD: './textures/characters/elephant.png',
    CharacterType.TOUGH: './textures/characters/panda.png',
    CharacterType.ARCHER: './textures/characters/penguin.png',
}


# Keyboard button keys defined inside pygame
button_keys = {
    'esc': 27,
}

# Colors
BLACK_RGB = (0,0,0)
WHITE_RGB = (255,255,255)
RED_RGB = (255,0,0)
DARK_GREEN_RGB = (98, 150, 113)

# Server parameters
db_name = "db/mydatabase.db"
default_players = 2
round_duration = 1 * 60

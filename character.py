"""
character.py
==================
Module provides representation for the game character
"""

import properties as pr
import pygame as pg

class Character(pg.sprite.Sprite):
    def __init__(self, sprite_group, grid_position, character_type):
        super().__init__(sprite_group)
        self.width = pr.hex_width // 2
        self.height = pr.hex_height // 2
        self.grid_position = grid_position
        self.update_character_type(character_type)

    def update_character_type(self, character_type):
        self.character_type = character_type
        self.texture = pg.image.load(pr.character_type2img[self.character_type])
        # self.texture = pg.transform.rotate(self.texture, 60)
        self.texture = pg.transform.scale(self.texture, (int(self.width), int(self.height)))

    def update(self, event):
        pass

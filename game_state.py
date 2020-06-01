"""
game_state.py
==================
Module provides representation for the in-game behaviour, board parameters, etc.
"""
import random
import pygame as pg

from gui import Button
import grid as grid_module
import character as character_module
import properties as pr


class GameState:
    def __init__(self):
        self.character_sprites = pg.sprite.Group()
        self.grid_sprites = pg.sprite.Group()
        self.button_sprites = pg.sprite.Group()

        characters = []
        for _ in range(5):
            h = random.randrange(0, pr.grid_height)
            w = random.randrange(0, pr.grid_width)
            cts = pr.CharacterType.type_names()
            ct_i = random.randrange(0, len(cts))
            characters.append(character_module.Character(sprite_group=self.character_sprites,
                                                         grid_position=(h, w),
                                                         character_type=pr.CharacterType[cts[ct_i]]))
        self.grid = grid_module.Grid(self.grid_sprites,
                                     pr.grid_width, pr.grid_height,
                                     pr.hex_edge_length, characters)

        self.menu_button = Button(self, (650,50), 'Back to menu', None)

    def update(self, event):
        self.game_finished = event.type == pg.QUIT or \
                (hasattr(event, 'key') and event.key == pr.button_keys['esc'])
        if not self.game_finished:
            self.grid_sprites.update(event)
            self.character_sprites.update(event)
            self.button_sprites.update(event)
        return self.game_finished

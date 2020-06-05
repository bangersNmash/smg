"""
game_state.py
==================
Module provides representation for the in-game behaviour, board parameters, etc.
"""
import random
import pygame as pg

from gui import Button, HexInfoWidget, SpriteGroup
import grid as grid_module
import character as character_module
import properties as pr


class GameState:
    def __init__(self):
        self.character_sprites = SpriteGroup()
        self.grid_sprites = SpriteGroup()
        self.button_sprites = SpriteGroup()
        self.infowidget_sprites = SpriteGroup()

        characters = []
        for _ in range(5):
            h = random.randrange(0, pr.grid_height)
            w = random.randrange(0, pr.grid_width)
            cts = pr.CharacterType.type_names()
            ct_i = random.randrange(0, len(cts))
            characters.append(character_module.Character(sprite_group=self.character_sprites,
                                                         grid_position=(h, w),
                                                         character_type=pr.CharacterType[cts[ct_i]]))

        self.grid_topleft_position = (pr.game_window_width // 4, pr.game_window_height // 4)
        self.bg_grid_surface = pg.Surface((pr.game_window_width // 2, pr.game_window_height // 2))
        self.bg_grid_surface_rect = self.bg_grid_surface.get_rect(topleft=self.grid_topleft_position)
        self.bg_grid_surface.fill(pr.WHITE_RGB)

        self.grid = grid_module.Grid(sprite_group=self.grid_sprites,
                                     bg_surface_data=(self.bg_grid_surface, self.bg_grid_surface_rect),
                                     width_in_hexes=pr.grid_width,
                                     height_in_hexes=pr.grid_height,
                                     hex_edge_length=pr.hex_edge_length,
                                     objects=characters)

        self.menu_button = Button(game_state=self,
                                  pos=(6 * pr.game_window_width // 8, 1 * pr.game_window_height // 8),
                                  text='Back to menu',
                                  action=None)
        self.hex_info_widget = HexInfoWidget(game_state=self,
                                             pos=(0, 1 * pr.game_window_height // 4),
                                             size=(pr.game_window_width // 6, pr.game_window_height // 4),
                                             action=None)

    def update(self, event):
        self.game_finished = event.type == pg.QUIT or \
                (hasattr(event, 'key') and event.key == pr.button_keys['esc'])
        if not self.game_finished:
            self.grid_sprites.update(event)
            self.character_sprites.update(event)
            self.button_sprites.update(event)
            self.infowidget_sprites.update()
        return self.game_finished

    def draw(self, screen):
        screen.fill(pr.BLACK_RGB)
        self.grid_sprites.draw(screen)
        # self.character_sprites.draw(screen)
        self.button_sprites.draw(screen)
        self.infowidget_sprites.draw(screen)

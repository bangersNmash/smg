import pygame

import properties as pr

class SpriteGroup(pygame.sprite.Group):
    def draw(self, surface):
        for sprite in self.sprites():
            sprite.draw(surface)

class Button(pygame.sprite.Sprite):
    def __init__(self, game_state, pos, text, action):
        super().__init__(game_state.button_sprites)
        self.game_state = game_state
        self.pos = pos
        self.action = action
        font = pygame.font.SysFont("Calibri", 24)
        self.text = font.render(text, True, pr.WHITE_RGB)
        self.width, self.height = self.text.get_size()
        self.width, self.height = self.width + 10, self.height + 10

        self.text_rect = self.text.get_rect(size=self.text.get_size(),
                                            center=(self.width // 2, self.height // 2))
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=pos)

        self.image.fill(pr.DARK_GREEN_RGB)
        self.image.blit(self.text, self.text_rect)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.game_state.game_finished = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class InfoWidget(pygame.sprite.Sprite):
    def __init__(self, game_state, pos, size, action):
        super().__init__(game_state.infowidget_sprites)
        self.game_state = game_state
        self.pos = pos
        self.action = action
        self.width, self.height = size
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(topleft=pos)

    def fill_widget(self):
        '''Set value for `self.image` according to the widget purpose'''
        self.image.fill(pr.DARK_GREEN_RGB)
    def update(self):
        self.fill_widget()
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class HexInfoWidget(InfoWidget):
    def fill_widget(self):
        observed_hex = self.game_state.grid.observed_hex
        font = pygame.font.SysFont("Calibri", 20)
        self.image.fill(pr.WHITE_RGB)
        if observed_hex is not None:
            hex_type = observed_hex.hex_type
            texture = observed_hex.texture
            texture_rect = texture.get_rect(size=texture.get_size(),
                                            center=(self.width // 2, self.height // 3))
            self.image.blit(texture, texture_rect)
            text = font.render(str(hex_type), True, pr.BLACK_RGB)
            text_rect = text.get_rect(size=text.get_size(),
                                      center=(self.width // 2, 3 * self.height // 4))
            self.image.blit(text, text_rect)
        else:
            text = font.render("Nothing to observe", True, pr.BLACK_RGB)
            text_rect = text.get_rect(size=text.get_size(),
                                      center=(self.width // 2, self.height // 2))
            self.image.blit(text, text_rect)
    def update(self):
        self.fill_widget()


def reset(menu, func):
    """Serves as a kind of decorator for functions connected with menu buttons,
    but it's not the real decorator because it takes dynamical menu argument as an input"""
    def new_func(*args, **kwargs):
        res = func(*args, **kwargs)
        menu.full_reset()
        print('Reset happened!')
        return res
    return new_func

def draw(screen, game_state):
    """Draws all game objects on given surface"""
    screen.fill(pr.BLACK_RGB)
    grid = game_state.grid
    grid_surface = grid.surface

    for h in grid.hexes():
        if h.hex_type == pr.HexType.PLAIN:
            pygame.draw.polygon(grid_surface, pr.WHITE_RGB, list(h.vertices.values()))
        else:
            grid_surface.blit(h.texture, h.hex_texture_corner_pos)
        if h.object is not None:
            grid_surface.blit(h.object.texture, h.object_texture_corner_pos)
        pygame.draw.aalines(grid_surface, pr.DARK_GREEN_RGB, True, list(h.vertices.values()))

    screen.blit(grid_surface, grid_surface.get_rect(center=(pr.game_window_width // 2,
                                                            pr.game_window_height // 2)))
    game_state.button_sprites.draw(screen)

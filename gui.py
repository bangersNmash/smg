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
        # frame_image(self.image)
        self.image.blit(self.text, self.text_rect)

    def update(self, event):
        if self.action is not None:
            self.action(self, event)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

def finish_game_action(button, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if button.rect.collidepoint(event.pos):
            button.game_state.game_finished = True

def end_turn_action(button, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if button.rect.collidepoint(event.pos):
            button.image.fill(pr.GREY_RGB)
            button.image.blit(button.text, button.text_rect)


class InfoWidget(pygame.sprite.Sprite):
    def __init__(self, game_state, pos, size, action):
        super().__init__(game_state.infowidget_sprites)
        self.game_state = game_state
        self.pos = pos
        self.width, self.height = size
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pr.WHITE_RGB)
        # frame_image(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.action = action
    def update(self):
        if self.action is not None:
            self.action(self)
    def draw(self, screen):
        screen.blit(self.image, self.rect)

def update_hex_infowidget(infowidget):
    observed_hex = infowidget.game_state.grid.observed_hex
    font = pygame.font.SysFont("Calibri", 20)
    infowidget.image.fill(pr.WHITE_RGB)
    if observed_hex is not None:
        h, w = infowidget.height, infowidget.width
        triplets = [(observed_hex, h // 4, str(observed_hex.hex_type))]
        if observed_hex.object is not None:
            triplets.append((observed_hex.object, 3 * h // 4, str(observed_hex.object.character_type)))
        for obj, oh, tl in triplets:
            texture = obj.texture.copy()
            if obj.height > h // 2:
                texture = pygame.transform.scale(texture,
                                                 (obj.width, h // 2))
            texture_rect = texture.get_rect(size=texture.get_size(),
                                            center=(1 * w // 4, oh))
            infowidget.image.blit(texture, texture_rect)
            text = font.render(tl, True, pr.BLACK_RGB)
            if text.get_width() > w // 2:
                text = pygame.transform.scale(text, (w // 2, text.get_height()))
            text_rect = text.get_rect(size=text.get_size(),
                                      center=(3 * w // 4, oh))
            infowidget.image.blit(text, text_rect)
    else:
        text = font.render("Nothing to observe", True, pr.BLACK_RGB)
        text_rect = text.get_rect(size=text.get_size(),
                                  center=(infowidget.width // 2, infowidget.height // 2))
        infowidget.image.blit(text, text_rect)

def update_initiative_order_infowidget(infowidget):
    characters = infowidget.game_state.get_character_initiative_order()
    font = pygame.font.SysFont("Calibri", 20)
    infowidget.image.fill(pr.WHITE_RGB)
    # w,h = characters[0].width, characters[0].height
    h_offset = 30

    for t,cp in [("Initiative order", (infowidget.width // 2, 10)),
                 ("(Character, Hex pos)", (infowidget.width // 2, 20))]:
        text = font.render(t, True, pr.BLACK_RGB)
        text_rect = text.get_rect(size=text.get_size(),
                                  center=cp)
        infowidget.image.blit(text, text_rect)

    h = (infowidget.height - h_offset) // len(characters)
    for i,c in enumerate(characters, start=1):
        texture = pygame.transform.scale(c.texture.copy(), (c.width, h))
        texture_rect = texture.get_rect(size=texture.get_size(),
                                        center=(1 * infowidget.width // 3, h_offset + i*h - h // 2))
        infowidget.image.blit(texture, texture_rect)
        text = font.render(str(c.grid_position), True, pr.BLACK_RGB)
        text_rect = text.get_rect(size=text.get_size(),
                                  center=(2 * infowidget.width // 3, h_offset + i * h - h // 2))
        infowidget.image.blit(text, text_rect)

def frame_image(image):
    w, h = image.get_size()
    pygame.draw.lines(image, pr.DARK_BROWN_RGB, True,
                      points=[(0, h), (0, 0), (w, 0), (w, h)],
                      width=5)


def reset(menu, func):
    """Serves as a kind of decorator for functions connected with menu buttons,
    but it's not the real decorator because it takes dynamical menu argument as an input"""
    def new_func(*args, **kwargs):
        res = func(*args, **kwargs)
        menu.full_reset()
        print('Reset happened!')
        return res
    return new_func

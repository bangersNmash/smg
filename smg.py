"""
smg.py -- the game
==================
Core module describing top level game logic.
"""
import pygame
import random
import pygame_menu as pgm

import grid as grid_module
import character as character_module
import game_state as game_state_module
from gui import reset
import properties as pr

tick_milliseconds = 100

def game():
    """Start game cycle"""
    draw_request_event_type = pygame.USEREVENT
    pygame.time.set_timer(draw_request_event_type, tick_milliseconds)
    screen = pygame.display.set_mode((pr.game_window_width, pr.game_window_height),
                                     pygame.RESIZABLE)
    pygame.display.set_caption('So damn good strategy...')

    game_state = game_state_module.GameState()
    game_finished = False

    while not game_finished:
        game_state.draw(screen)

        event = pygame.event.wait()
        # print(event)
        if event.type == draw_request_event_type:
            pygame.display.flip()
        else:
            game_finished = game_state.update(event)
    print('Game finished!')

def menu():
    menu_surface = pygame.display.set_mode((pr.menu_window_width, pr.menu_window_height),
                                           flags=pygame.RESIZABLE)

    menu = pgm.Menu(pr.menu_window_width, pr.menu_window_height, 'Welcome',
             theme=pgm.themes.THEME_SOLARIZED,
             column_force_fit_text=True)

    menu.add_text_input('Name: ', default='<type your nickname here>')
    menu.add_button('Play Random Game', reset(menu,game))
    menu.add_button('Create Game', reset(menu,game))
    menu.add_button('Join Game', reset(menu,game))
    menu.add_button('Quit', pgm.events.EXIT)
    menu.mainloop(menu_surface)

def main():
    pygame.init()
    menu()

if __name__ == '__main__':
    main()

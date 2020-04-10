import pygame.event

import smg


def test_handle_event_quit():
    quit_event = pygame.event.Event(pygame.QUIT, dict={})
    assert not smg.handle_event(quit_event)


def test_handle_event_not_quit():
    not_quit_event = pygame.event.Event(pygame.K_w, dict={})
    assert smg.handle_event(not_quit_event)

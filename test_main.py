import pygame.event

import smg


def test_handle_event_quit():
    quit_event = smg.handle_event(pygame.event.Event(pygame.QUIT, dict={}))
    assert quit_event == smg.finish


def test_handle_event_not_quit():
    not_quit_event = smg.handle_event(pygame.event.Event(pygame.K_w, dict={}))
    assert not_quit_event != smg.finish

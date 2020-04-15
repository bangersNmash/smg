"""
test_main.py -- tests smg.py
============================
Contains tests for high level game logic.
"""
import pygame.event

import smg


def test_handle_event_quit():
    """smg.handle_event should return correct handler for QUIT action"""
    quit_event = smg.handle_event(pygame.event.Event(pygame.QUIT, dict={}))
    assert quit_event == smg.finish


def test_handle_event_not_quit():
    """smg.handle_event should return correct handler for QUIT action"""
    not_quit_event = smg.handle_event(pygame.event.Event(pygame.K_w, dict={}))
    assert not_quit_event != smg.finish

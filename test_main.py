import unittest

import pygame.event

import smg


class TestMain(unittest.TestCase):

    def test_handle_event_quit(self):
        quit_event = pygame.event.Event(pygame.QUIT, dict={})
        assert not smg.handle_event(quit_event)

    def test_handle_event_not_quit(self):
        not_quit_event = pygame.event.Event(pygame.K_w, dict={})
        assert smg.handle_event(not_quit_event)


if __name__ == '__main__':
    unittest.main()

from pico2d import *
import game_framework
import game_world
import game_data

class PlayerOne:
    def __init__(self, character_index):
        self.select_char = character_index

    def handle_event(self, event):
        if event.key in (SDLK_w, SDLK_s, SDLK_a, SDLK_d, SDLK_q, SDLK_e):
            self.select_char.handle_event(event)


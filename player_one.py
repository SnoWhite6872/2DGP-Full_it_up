from pico2d import *
import game_framework
import game_world
import game_data

class PlayerOne:
    def __init__(self, character_index):
        self.select_char = character_index

    def handle_events(self, event):

        self.select_char.handle_event(event)


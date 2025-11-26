from pico2d import *
import game_framework
import game_world
import game_data

class PlayerTwo:
    def __init__(self, character_index):
        self.select_char = character_index

    def handle_events(self, event):
        events_list = get_events()
        for event in events_list:
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_UP:
                    event.key = SDLK_w
                elif event.key == SDLK_DOWN:
                    event.key = SDLK_s
                elif event.key == SDLK_LEFT:
                    event.key = SDLK_a
                elif event.key == SDLK_RIGHT:
                    event.key = SDLK_d
                elif event.key == SDLK_m:
                    event.key = SDLK_q
                elif event.key == SDLK_n:
                    event.key = SDLK_e

            elif event.type == SDL_KEYUP:
                if event.key == SDLK_UP:
                    event.key = SDLK_w
                elif event.key == SDLK_DOWN:
                    event.key = SDLK_s
                elif event.key == SDLK_LEFT:
                    event.key = SDLK_a
                elif event.key == SDLK_RIGHT:
                    event.key = SDLK_d
                elif event.key == SDLK_m:
                    event.key = SDLK_q
                elif event.key == SDLK_n:
                    event.key = SDLK_e


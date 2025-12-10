from pico2d import *


class PlayerTwo:
    def __init__(self, character_index):
        self.select_char = character_index

    def handle_event(self, event):
        if event.key in (SDLK_UP, SDLK_DOWN, SDLK_LEFT, SDLK_RIGHT, SDLK_n, SDLK_m, SDLK_b):
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
                elif event.key == SDLK_b:
                    event.key = SDLK_r

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
                elif event.key == SDLK_b:
                    event.key = SDLK_r

            self.select_char.handle_event(event)


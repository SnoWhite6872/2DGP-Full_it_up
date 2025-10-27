from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_w, SDLK_a, SDLK_s, SDLK_d
from state_machine import StateMachine


def a_down(e):
    return e[0] == 'IMPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def d_down(e):
    return e[0] == 'IMPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d
def w_down(e):
    return e[0] == 'IMPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w
def s_down(e):
    return e[0] == 'IMPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def a_up(e):
    return e[0] == 'IMPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a
def d_up(e):
    return e[0] == 'IMPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d
def w_up(e):
    return e[0] == 'IMPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w
def s_up(e):
    return e[0] == 'IMPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s


class Idle:
    def __init__(self, chacat):
        self.chacat = chacat

    def enter(self,e):
        pass

    def exit(self,e):
        pass

    def do(self):
        pass

    def draw(self):
        pass

class Chacat:
    def __init__(self):
        self.image = load_image('Cha_cat.png')
        self.x, self.y = 300, 400
        self.w_dir = 0
        self.h_dir = 0

        #self.state_machine = StateMachine()
        pass


    def update(self):
        pass

    def draw(self):
        pass

    def handle_events(self, event):
        #self.state_machine.handle_state_event(event)
        pass
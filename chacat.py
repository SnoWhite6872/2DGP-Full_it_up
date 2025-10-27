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

class Run:
    def __init__(self, chacat):
        self.chacat = chacat

    def enter(self,e):
        if d_down(e) or a_up(e):
            self.chacat.w_dir = 1  #오른쪽 이동
        elif a_down(e) or d_up(e):
            self.chacat.w_dir = -1
        pass

    def exit(self,e):
        pass

    def do(self):
        self.chacat.x += self.chacat.w_dir * 5
        pass

    def draw(self):
        self.chacat.image.draw(self.chacat.x, self.chacat.y)


class Idle:
    def __init__(self, chacat):
        self.chacat = chacat


    def enter(self,e):
        self.chacat.w_dir = 0
        pass

    def exit(self,e):
        pass

    def do(self):
        pass

    def draw(self):
        self.chacat.image.draw(self.chacat.x, self.chacat.y)
        pass

class Chacat:
    def __init__(self):
        self.image = load_image('Cha_cat.png')
        self.x, self.y = 200, 400
        self.w_dir = 0
        self.h_dir = 0

        self.RUN = Run(self)
        self.IDLE = Idle(self)

        self.state_machine = StateMachine(
            self.IDLE,
        {
            self.IDLE : {d_down: self.RUN, a_down: self.RUN},
            self.RUN : {d_up: self.IDLE, a_up: self.IDLE, d_down : self.IDLE, a_down: self.IDLE}

            }
        )
        pass


    def update(self):
        self.state_machine.update()
        pass

    def draw(self):
        self.state_machine.draw()
        pass

    def handle_event(self, event):
        self.state_machine.handle_state_event(('IMPUT',event))
        pass
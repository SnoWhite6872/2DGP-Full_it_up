from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_w, SDLK_a, SDLK_s, SDLK_d
from state_machine import StateMachine


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a
def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d
def w_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w
def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a
def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d
def w_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w
def s_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s

class WRun:
    def __init__(self, chacat):
        self.chacat = chacat

    def enter(self,e):
        if d_down(e) or a_up(e):
            self.chacat.w_dir = 1  #오른쪽 이동
        elif a_down(e) or d_up(e):
            self.chacat.w_dir = -1
        elif w_up(e) or s_up(e):
            self.chacat.h_dir = 0

    def exit(self,e):
        pass

    def do(self):
        self.chacat.x += self.chacat.w_dir * 1
        self.chacat.y += self.chacat.h_dir * 1
        pass

    def draw(self):
        self.chacat.image.draw(self.chacat.x, self.chacat.y)

class HRun:
        def __init__(self, chacat):
            self.chacat = chacat

        def enter(self,e):
            if w_down(e) or s_up(e):
                self.chacat.h_dir = 1
            elif s_down(e) or w_up(e):
                self.chacat.h_dir = -1
            elif a_up(e) or d_up(e):
                self.chacat.w_dir = 0

        def exit(self,e):
            pass

        def do(self):
            self.chacat.x += self.chacat.w_dir * 1
            self.chacat.y += self.chacat.h_dir * 1
            pass

        def draw(self):
            self.chacat.image.draw(self.chacat.x, self.chacat.y)


class Idle:
    def __init__(self, chacat):
        self.chacat = chacat


    def enter(self,e):
        self.chacat.w_dir = 0
        self.chacat.h_dir = 0
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

        self.WRUN = WRun(self)
        self.HRUN = HRun(self)
        self.IDLE = Idle(self)

        self.state_machine = StateMachine(
            self.IDLE,
        {
            self.IDLE : {d_down: self.WRUN, a_down: self.WRUN, w_down : self.HRUN , s_down : self.HRUN, w_up: self.HRUN, s_up : self.HRUN, a_up : self.WRUN, d_up : self.WRUN},
            self.WRUN : {d_up: self.IDLE, a_up: self.IDLE, d_down : self.IDLE, a_down: self.IDLE, w_up : self.WRUN, s_up : self.WRUN, w_down : self.HRUN, s_down : self.HRUN},
            self.HRUN : {w_up : self.IDLE, s_up : self.IDLE, w_down : self.IDLE, s_down : self.IDLE, a_up : self.HRUN, d_up : self.HRUN, a_down : self.WRUN, d_down : self.WRUN},

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
        self.state_machine.handle_state_event(('INPUT', event))
        pass
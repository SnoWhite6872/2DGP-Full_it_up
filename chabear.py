from pico2d import load_image
from sdl2 import SDL_KEYUP, SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN
from state_machine import StateMachine

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT




class Run:
    def __init__(self, chabear):
        self.chabear = chabear
    def enter(self,e):
        if right_down(e) or left_up(e):
            self.chabear.w_dir = 1  #오른쪽 이동 +
        elif left_down(e) or right_up(e):
            self.chabear.w_dir = -1

        pass

    def exit(self,e):
        pass
    def do(self):
        self.chabear.x += self.chabear.w_dir *5
        self.chabear.y += self.chabear.h_dir * 5
        pass
    def draw(self):
        self.chabear.image.draw(self.chabear.x, self.chabear.y)

class Idle():
    def __init__(self, chabear):
        self.chabear = chabear
    def enter(self,e):
        self.chabear.w_dir = 0
        self.chabear.h_dir = 0
        pass

    def exit(self,e):
        pass

    def do(self):
        pass

    def draw(self):
        self.chabear.image.draw(self.chabear.x, self.chabear.y)


class Chabear:
    def __init__(self):
        self.image = load_image('Cha_bear.png')
        self.x, self.y = 252, 525
        self.w_dir = 0
        self.h_dir = 0

        self.RUN = Run(self)
        self.IDLE = Idle(self)

        self.state_machine = StateMachine(
            self.IDLE,               #시작 state
        {
            self.IDLE : { left_down : self.RUN, right_down: self.RUN},
            self.RUN : { left_up : self.IDLE, right_up: self.IDLE},
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
        self.state_machine.handle_state_event(('INPUT',event))
        pass

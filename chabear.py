from pico2d import load_image, get_events
from sdl2 import SDL_KEYUP, SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN
from state_machine import StateMachine

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP
def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP
def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN



class WRun:
    def __init__(self, chabear):
        self.chabear = chabear
    def enter(self,e):
        if right_down(e) or left_up(e):
            self.chabear.w_dir = 1  #오른쪽 이동
        elif left_down(e) or right_up(e):
            self.chabear.w_dir = -1

    def exit(self,e):
        pass
    def do(self):
        self.chabear.x += self.chabear.w_dir * 5
        self.chabear.y += self.chabear.h_dir * 5
        pass
    def draw(self):
        self.chabear.image.draw(self.chabear.x, self.chabear.y)

class HRun:
    def __init__(self, chabear):
        self.chabear = chabear

    def enter(self,e):
        if up_down(e) or down_up(e):
            self.chabear.h_dir = 1
        elif down_down(e) or up_up(e):
            self.chabear.h_dir = -1

    def exit(self,e):
        pass

    def do(self):
        self.chabear.x += self.chabear.w_dir * 5
        self.chabear.y += self.chabear.h_dir * 5
        pass

    def draw(self):
        self.chabear.image.draw(self.chabear.x, self.chabear.y)

# class DRun:
#     def __init__(self, chabear):
#         self.chabear = chabear
#
#     def enter(self,e):
#         events = get_events()
#         for event in events:
#             if event.type == SDL_KEYDOWN:
#                 if event.key == SDLK_UP:
#                     if event.key == SDLK_RIGHT:
#                         self.chabear.h_dir = 1
#                         self.chabear.w_dir = 1
#                     elif event.key == SDLK_LEFT:
#                         self.chabear.h_dir = 1
#                         self.chabear.w_dir = -1
#                 elif event.key == SDLK_DOWN:
#                     if event.key == SDLK_RIGHT:
#                         self.chabear.h_dir = -1
#                         self.chabear.w_dir = 1
#                     elif event.key == SDLK_LEFT:
#                         self.chabear.h_dir = -1
#                         self.chabear.w_dir = -1
#
#     def exit(self,e):
#         pass
#
#     def do(self):
#         self.chabear.x += self.chabear.w_dir * 5
#         self.chabear.y += self.chabear.h_dir * 5
#         pass
#
#     def draw(self):
#         self.chabear.image.draw(self.chabear.x, self.chabear.y)

class Idle:
    def __init__(self, chabear):
        self.chabear = chabear
    def enter(self,e):
        self.chabear.w_dir = 0
        self.chabear.h_dir = 0
        pass

    def exit(self,e):
        pass

    def do(self):
        self.chabear.w_dir = 0
        self.chabear.h_dir = 0
        pass

    def draw(self):
        self.chabear.image.draw(self.chabear.x, self.chabear.y)


class Chabear:
    def __init__(self):
        self.image = load_image('Cha_bear.png')
        self.x, self.y = 100, 200
        self.w_dir = 0
        self.h_dir = 0

        self.WRUN = WRun(self)
        self.HRUN = HRun(self)
        # self.DRUN = DRun(self)
        self.IDLE = Idle(self)

        self.state_machine = StateMachine(
            self.IDLE,               #시작 state
        {
            self.IDLE : { left_down : self.WRUN, right_down: self.WRUN, left_up: self.WRUN, right_up: self.WRUN, up_down: self.HRUN, down_down: self.HRUN},
            self.WRUN : { left_up : self.IDLE, right_up: self.IDLE, left_down: self.IDLE, right_down: self.IDLE, up_down: self.HRUN, down_down: self.HRUN},
            self.HRUN : { up_up : self.IDLE, down_up: self.IDLE, up_down: self.IDLE, down_down: self.IDLE, left_down: self.WRUN, right_down: self.WRUN},
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

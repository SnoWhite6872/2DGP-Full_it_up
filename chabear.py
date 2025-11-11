from pico2d import load_image, get_events
from sdl2 import SDL_KEYUP, SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_m
from state_machine import StateMachine

def event_stop(e):
    return e[0] == 'STOP'

def event_run(e):
    return e[0] == 'RUN'

def m_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_m



# class WRun:
#     def __init__(self, chabear):
#         self.chabear = chabear
#     def enter(self,e):
#         if right_down(e) or left_up(e):
#             self.chabear.w_dir = 1  #오른쪽 이동
#         elif left_down(e) or right_up(e):
#             self.chabear.w_dir = -1
#         elif up_up(e) or down_up(e):
#             self.chabear.h_dir = 0
#
#     def exit(self,e):
#         pass
#     def do(self):
#         self.chabear.x += self.chabear.w_dir * 1
#         self.chabear.y += self.chabear.h_dir * 1
#         pass
#     def draw(self):
#         self.chabear.image.draw(self.chabear.x, self.chabear.y)

class HRun:
    def __init__(self, chabear):
        self.chabear = chabear

    def enter(self,e):
        if self.chabear.w_dir != 0:                   #가로 방향이 0이 아니면 가로 방향은 시선 방향과 같다.
            self.chabear.f_dir = self.chabear.w_dir


    def exit(self,e):
        pass

    def do(self):
        self.chabear.x += self.chabear.w_dir * 1
        self.chabear.y += self.chabear.h_dir * 1
        pass

    def draw(self):
        self.chabear.image.draw(self.chabear.x, self.chabear.y)


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
        pass

    def draw(self):
        self.chabear.image.draw(self.chabear.x, self.chabear.y)


class Chabear:
    def __init__(self):
        self.image = load_image('Cha_bear.png')
        self.x, self.y = 100, 200
        self.w_dir = 0
        self.h_dir = 0
        self.f_dir = 1

        self.WRUN = WRun(self)
        self.HRUN = HRun(self)
        # self.DRUN = DRun(self)
        self.IDLE = Idle(self)

        self.state_machine = StateMachine(
            self.IDLE,               #시작 state
        {
            self.IDLE : { m_down: self.IDLE ,left_down : self.WRUN, right_down: self.WRUN, left_up: self.WRUN, right_up: self.WRUN, up_down: self.HRUN, down_down: self.HRUN, up_up : self.HRUN, down_up : self.HRUN},
            self.WRUN : { m_down: self.WRUN ,left_up : self.IDLE, right_up: self.IDLE, left_down: self.IDLE, right_down: self.IDLE, up_down: self.HRUN, down_down: self.HRUN, up_up : self.WRUN, down_up : self.WRUN},
            self.HRUN : { m_down: self.HRUN ,up_up : self.IDLE, down_up: self.IDLE, up_down: self.IDLE, down_down: self.IDLE, left_down: self.WRUN, right_down: self.WRUN, right_up : self.HRUN, left_up : self.HRUN},
            }
        )

    def draw(self):
        if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN):
            cur_xdir, cur_ydir = self.w_dir, self.h_dir

    def update(self):
        self.state_machine.update()




    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))


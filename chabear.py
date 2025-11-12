from pico2d import *
from sdl2 import SDL_KEYUP, SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_m
from state_machine import StateMachine



def event_stop(e):
    return e[0] == 'STOP'

def event_run(e):
    return e[0] == 'RUN'

def m_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_m

class WAttack:
        def __init__(self, chabear):
            self.chabear = chabear
            self.timer = 0

        def enter(self, e):
            if m_down(e):
                print("2P 공격")
            self.timer = 30

        def exit(self, e):
            pass

        def do(self):
            self.chabear.x += self.chabear.x_dir * 1
            self.chabear.y += self.chabear.y_dir * 1
            self.timer -= 1
            if self.timer <= 0:
                self.chabear.state_machine.handle_state_event(('RUN', 0))

        def draw(self):
            self.chabear.image.draw(self.chabear.x, self.chabear.y)
            pass

class Run:
    def __init__(self, chabear):
        self.chabear = chabear

    def enter(self,e):
        if self.chabear.x_dir != 0:                   #가로 방향이 0이 아니면 가로 방향은 시선 방향과 같다.
            self.chabear.f_dir = self.chabear.y_dir


    def exit(self,e):
        pass

    def do(self):
        self.chabear.x += self.chabear.x_dir * 1
        self.chabear.y += self.chabear.y_dir * 1
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
        self.x_dir = 0
        self.y_dir = 0
        self.f_dir = 1


        self.RUN = Run(self)
        self.IDLE = Idle(self)
        self.WATTACK = WAttack(self)

        self.state_machine = StateMachine(
            self.IDLE,               #시작 state
        {

                self.IDLE: { m_down: self.WATTACK,event_run: self.RUN},
                self.RUN: {m_down: self.WATTACK,event_stop: self.IDLE},
                self.WATTACK : {event_stop: self.IDLE, event_run: self.RUN}
            }
        )
    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if event.key in (SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN):
            cur_xdir , cur_ydir = self.x_dir, self.y_dir
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_RIGHT:
                        self.x_dir += 1
                elif event.key == SDLK_LEFT:
                        self.x_dir += -1
                elif event.key == SDLK_UP:
                        self.y_dir += 1
                elif event.key == SDLK_DOWN:
                        self.y_dir += -1
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_RIGHT:
                    self.x_dir += -1
                elif event.key == SDLK_LEFT:
                    self.x_dir += 1
                elif event.key == SDLK_UP:
                    self.y_dir += -1
                elif event.key == SDLK_DOWN:
                    self.y_dir += 1
            if cur_xdir != self.x_dir or cur_ydir != self.y_dir:
                if self.x_dir == 0 and self.y_dir == 0:
                        self.state_machine.handle_state_event(('STOP', self.f_dir))
                else:
                        self.state_machine.handle_state_event(('RUN', None))
        else:
            self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 35, self.y - 60, self.x + 35, self.y + 40







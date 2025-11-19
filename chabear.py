from pico2d import *
from sdl2 import SDL_KEYUP, SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_m, SDLK_n
from state_machine import StateMachine
from cookie import Cookie
import game_world
import game_framework


PIXEL_PER_METER = (1.0 / 0.03)  # 10픽셀 30센치미터
RUN_SPEED_KMPH = 50.0  # 시속 20킬로미터
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0) # 분속
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)        # 초속
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  #달리기 픽셀 속도


TIME_PER_ACTION = 1.0         #1초 액션 당 걸리는 시간
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_IDLE = 5

bear_animation_names = ['Idle', 'Run', 'Touch']


def event_stop(e):
    return e[0] == 'STOP'

def event_run(e):
    return e[0] == 'RUN'

def m_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_m

def n_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_n

class WAttack:
        def __init__(self, chabear):
            self.chabear = chabear
            self.timer = 0

        def enter(self, e):
            if self.chabear.x_dir != 0:
                self.chabear.f_dir = self.chabear.x_dir

            self.timer = 300

        def exit(self, e):
            pass

        def do(self):
            # self.chabear.x += self.chabear.x_dir * RUN_SPEED_PPS * game_framework.frame_time
            # self.chabear.y += self.chabear.y_dir * RUN_SPEED_PPS * game_framework.frame_time
            self.chabear.frame = (self.chabear.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 2
            self.timer -= 1
            if self.timer <= 0:
                self.chabear.state_machine.handle_state_event(('STOP', None))

        def draw(self):
            self.chabear.images['Touch'][1].draw(self.chabear.x, self.chabear.y, 100, 120)
            pass

class Run:
    def __init__(self, chabear):
        self.chabear = chabear

    def enter(self,e):
        if self.chabear.x_dir != 0:                   #가로 방향이 0이 아니면 가로 방향은 시선 방향과 같다.
            self.chabear.f_dir = self.chabear.x_dir


    def exit(self,e):
        if( n_down(e)):
            self.chabear.throw_cookie()
        pass

    def do(self):
        self.chabear.x += self.chabear.x_dir * RUN_SPEED_PPS * game_framework.frame_time
        self.chabear.y += self.chabear.y_dir * RUN_SPEED_PPS * game_framework.frame_time
        self.chabear.frame = (self.chabear.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 2
        pass

    def draw(self):
        self.chabear.images['Run'][int(self.chabear.frame)].draw(self.chabear.x, self.chabear.y, 100, 120)


class Idle:
    def __init__(self, chabear):
        self.chabear = chabear
    def enter(self,e):
        if event_stop(e):
            self.chabear.f_dir = e[1]

    def exit(self,e):
        if( n_down(e)):
            self.chabear.throw_cookie()
        pass

    def do(self):
        self.chabear.frame = (self.chabear.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 2
        pass

    def draw(self):
        self.chabear.images['Idle'][int(self.chabear.frame)].draw(self.chabear.x, self.chabear.y, 100, 120)



class Chabear:
    images = None
    def __init__(self):
        self.hp = 0
        self.load_images()
        self.x, self.y = 100, 200
        self.x_dir = 0
        self.y_dir = 0
        self.f_dir = 1
        self.frame = 0
        game_world.add_collision_pair('chabear:cookie', self, None)


        self.RUN = Run(self)
        self.IDLE = Idle(self)
        self.WATTACK = WAttack(self)

        self.state_machine = StateMachine(
            self.IDLE,               #시작 state
        {

                self.IDLE: {n_down: self.IDLE, m_down: self.WATTACK,event_run: self.RUN},
                self.RUN: {n_down: self.RUN, m_down: self.WATTACK,event_stop: self.IDLE},
                self.WATTACK : { event_stop : self.IDLE}
            }
        )

    def load_images(self):
        if Chabear.images == None:
            Chabear.images = {}
            for name in bear_animation_names:
                Chabear.images[name] = [load_image("./Cha_bear/" + name + " (%d)" % i + ".png") for i in range(1, 3)]


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

    def throw_cookie(self):
        cookie = Cookie(self.x, self.y, self.f_dir * 25)
        game_world.add_object(cookie, 1)
        game_world.add_collision_pair('chacat:cookie', None, cookie)

        pass

    def handle_collision(self, group, other):
            if group == 'chabear:cookie':
                self.hp += 10
                print('bear hp + 10')

from pico2d import *
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_w, SDLK_a, SDLK_s, SDLK_d, SDLK_q, SDLK_e
from state_machine import StateMachine
from cookie import Cookie
import game_framework
import game_world
import game_data


def event_stop(e):
    return e[0] == 'STOP'

def event_run(e):
    return e[0] == 'RUN'

def q_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_q #1p 약공격

def e_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_e

def event_touch(e):
    return e[0] == 'TOUCH'

PIXEL_PER_METER = (1.0 / 0.03)  # 10픽셀 30센치미터
RUN_SPEED_KMPH = 50.0  # 시속 20킬로미터
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0) # 분속
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)        # 초속
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  #달리기 픽셀 속도

TIME_PER_ACTION = 1.0         #1초 액션 당 걸리는 시간
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_IDLE = 5
FRAMES_PER_TOUCH = 5

cat_animation_names = ['Idle', 'Run', 'Touch']

class Touch:
    def __init__(self, chacat):
        self.chacat = chacat
        self.time =0

    def enter(self, e):
        self.time = get_time()

    def exit(self,e):
        pass

    def do(self):
        self.chacat.frame = (self.chacat.frame + FRAMES_PER_TOUCH * ACTION_PER_TIME * game_framework.frame_time) % 2
        if get_time() - self.time >= 1:
            self.chacat.state_machine.handle_state_event(('STOP', None))
        pass

    def draw(self):
        if self.chacat.f_dir == -1:
            self.chacat.images['Touch'][1].draw(self.chacat.x, self.chacat.y, 100, 120)
        else:
            self.chacat.images['Touch'][1].composite_draw(0, 'h',self.chacat.x, self.chacat.y, 100, 120)

class WAttack:
        def __init__(self, chacat):
            self.chacat = chacat
            self.timer = 0

        def enter(self,e):
            if self.chacat.x_dir != 0:
                self.chacat.f_dir = self.chacat.x_dir
            self.timer = 300

        def exit(self,e):
            pass

        def do(self):
            self.chacat.x += self.chacat.x_dir * RUN_SPEED_PPS * game_framework.frame_time
            self.chacat.y += self.chacat.y_dir * RUN_SPEED_PPS * game_framework.frame_time
            self.timer -= 1
            if self.timer <= 0:
                self.chacat.state_machine.handle_state_event(('RUN', None))

            self.chacat.frame = (self.chacat.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 2

        def draw(self):
            if self.chacat.f_dir == -1:
                self.chacat.images['Touch'][int(self.chacat.frame)].draw(self.chacat.x, self.chacat.y, 100, 120)
            else:
                self.chacat.images['Touch'][int(self.chacat.frame)].composite_draw(0, 'h', self.chacat.x, self.chacat.y,100, 120)
            pass



class Run:
        def __init__(self, chacat):
            self.chacat = chacat

        def enter(self,e):
            if self.chacat.x_dir != 0:
                self.chacat.f_dir = self.chacat.x_dir

        def exit(self,e):
            if e_down(e):
                self.chacat.throw_cookie()
            pass

        def do(self):
            self.chacat.x += self.chacat.x_dir * RUN_SPEED_PPS * game_framework.frame_time
            self.chacat.y += self.chacat.y_dir * RUN_SPEED_PPS * game_framework.frame_time
            self.chacat.frame = (self.chacat.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 2

            pass

        def draw(self):
            if self.chacat.f_dir == -1:
                self.chacat.images['Run'][int(self.chacat.frame)].draw(self.chacat.x, self.chacat.y, 100, 120)
            else:
                self.chacat.images['Run'][int(self.chacat.frame)].composite_draw(0, 'h', self.chacat.x, self.chacat.y,100, 120)


class Idle:
    def __init__(self, chacat):
        self.chacat = chacat


    def enter(self,e):
        if event_stop(e):
            self.chacat.f_dir = e[1]
        pass

    def exit(self,e):
        if e_down(e):
            self.chacat.throw_cookie()
        pass

    def do(self):
        self.chacat.frame = (self.chacat.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 2
        pass

    def draw(self):
        if self.chacat.f_dir == -1:
            self.chacat.images['Idle'][int(self.chacat.frame)].draw(self.chacat.x, self.chacat.y, 100, 120)
        else:
            self.chacat.images['Idle'][int(self.chacat.frame)].composite_draw(0, 'h',self.chacat.x, self.chacat.y, 100, 120)
        pass

class Chacat:
    images = None
    def __init__(self):
        self.load_images()
        self.hp = 0
        self.x, self.y = 100, 700
        self.x_dir = 0
        self.y_dir = 0
        self.f_dir = 1
        self.frame = 0
        self.cookie_count = 0
        self.load_time = get_time()

        game_world.add_collision_pair('chacat:cookie', self, None)
        game_world.add_collision_pair('chacat:icetea', self, None)

        self.TOUCH = Touch(self)
        self.font = load_font('ENCR10B.TTF', 16)
        self.RUN = Run(self)
        self.IDLE = Idle(self)
        self.WATTACK = WAttack(self)

        self.state_machine = StateMachine(
            self.IDLE,
        {
            self.IDLE: {event_touch: self.TOUCH,e_down: self.IDLE,q_down: self.WATTACK, event_run : self.RUN},
            self.RUN: {event_touch: self.TOUCH, e_down:self.RUN,q_down: self.WATTACK, event_stop : self.IDLE},
            self.WATTACK : {event_stop: self.IDLE},
            self.TOUCH : { event_stop : self.IDLE}

            }
        )
        pass

    def load_images(self):
        if Chacat.images == None:
            Chacat.images = {}
            for name in cat_animation_names:
                Chacat.images[name] = [load_image("./Cha_cat/" + name + " (%d)" % i + ".png") for i in range(1, 3)]


    def update(self):
        self.state_machine.update()
        if get_time() - self.load_time > 2 and self.cookie_count < 4:
            self.cookie_count += 1
            self.load_time = get_time()
        if self.hp <= 0:
            self.hp = 0
        game_data.player1_hp = self.hp
        pass

    def draw(self):
        self.state_machine.draw()
        self.font.draw(self.x-10, self.y + 50, f'{self.hp:02d}', (255, 255, 255))
        draw_rectangle(*self.get_bb())
        pass

    def handle_event(self, event):
        if event.key in (SDLK_a, SDLK_d, SDLK_w, SDLK_s):
            cur_xdir , cur_ydir = self.x_dir, self.y_dir
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_d:
                        self.x_dir += 1
                elif event.key == SDLK_a:
                        self.x_dir += -1
                elif event.key == SDLK_w:
                        self.y_dir += 1
                elif event.key == SDLK_s:
                        self.y_dir += -1
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_d:
                    self.x_dir += -1
                elif event.key == SDLK_a:
                    self.x_dir += 1
                elif event.key == SDLK_w:
                    self.y_dir += -1
                elif event.key == SDLK_s:
                    self.y_dir += 1
            if cur_xdir != self.x_dir or cur_ydir != self.y_dir:
                if self.x_dir == 0 and self.y_dir == 0:
                        self.state_machine.handle_state_event(('STOP', self.f_dir))
                else:
                        self.state_machine.handle_state_event(('RUN', None))
        else:
            self.state_machine.handle_state_event(('INPUT', event))

    def throw_cookie(self):
        cookie = Cookie(self.x, self.y, self.f_dir * 25)
        game_world.add_object(cookie, 1)
        game_world.add_collision_pair('chabear:cookie', None, cookie)



    def get_bb(self):
        return self.x - 35, self.y - 60, self.x + 35, self.y + 40

    def handle_collision(self, group, other):
        if group == 'chacat:cookie':
            self.hp += 10
            print('cat hp + 10')
            self.state_machine.handle_state_event(('TOUCH', None))
        if group == 'chacat:icetea':
            self.hp -= 15

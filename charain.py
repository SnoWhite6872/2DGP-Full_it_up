from pico2d import *
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_w, SDLK_a, SDLK_s, SDLK_d, SDLK_q, SDLK_e
from state_machine import StateMachine
from cookie import Cookie
from attack import Attack
import game_framework
import game_world
import game_data

time_out = lambda e: e[0] == 'TIMEOUT'

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
RUN_SPEED_KMPH = 50.0  # 시속 50킬로미터
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0) # 분속
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)        # 초속
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  #달리기 픽셀 속도

TIME_PER_ACTION = 1.0         #1초 액션 당 걸리는 시간
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_IDLE = 5
FRAMES_PER_TOUCH = 5

rain_animation_names = ['Idle', 'Run', 'Touch']

class Touch:
    def __init__(self, charain):
        self.charain = charain
        self.time =0

    def enter(self, e):
        self.time = get_time()

    def exit(self,e):
        pass

    def do(self):
        self.charain.frame = (self.charain.frame + FRAMES_PER_TOUCH * ACTION_PER_TIME * game_framework.frame_time) % 2
        if get_time() - self.time >= 1:
            self.charain.state_machine.handle_state_event(('STOP', self.charain.f_dir))
        pass

    def draw(self):
        if self.charain.f_dir == -1:
            self.charain.images['Touch'][1].draw(self.charain.x, self.charain.y, 110, 125)
        else:
            self.charain.images['Touch'][1].composite_draw(0, 'h',self.charain.x, self.charain.y, 100, 120)

class WAttack:
        def __init__(self, charain):
            self.charain = charain
            self.timer = 0

        def enter(self,e):
            if self.charain.x_dir != 0:
                self.charain.f_dir = self.charain.x_dir
            self.timer = get_time()
            self.charain.attack()

        def exit(self,e):
            pass

        def do(self):
            # self.charain.x += self.charain.x_dir * RUN_SPEED_PPS * game_framework.frame_time
            # self.charain.y += self.charain.y_dir * RUN_SPEED_PPS * game_framework.frame_time
            self.timer -= 1
            if get_time() - self.timer >= 0.5:
                self.charain.state_machine.handle_state_event(('TIMEOUT', self.charain.f_dir))

            self.charain.frame = (self.charain.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 2

        def draw(self):
            if self.charain.f_dir == -1:
                self.charain.images['Run'][int(self.charain.frame)].draw(self.charain.x, self.charain.y, 100, 120)
            else:
                self.charain.images['Run'][int(self.charain.frame)].composite_draw(0, 'h', self.charain.x, self.charain.y,100, 120)
            pass



class Run:
        def __init__(self, charain):
            self.charain = charain

        def enter(self,e):
            pass

        def exit(self,e):
            if e_down(e):
                self.charain.throw_cookie()
            pass

        def do(self):
            speed = RUN_SPEED_PPS

            if self.charain.speed_boost:
                speed *= 2

            if self.charain.x_dir != 0:
                self.charain.f_dir = self.charain.x_dir
            self.charain.x += self.charain.x_dir * speed * game_framework.frame_time
            self.charain.y += self.charain.y_dir * speed * game_framework.frame_time
            self.charain.frame = (self.charain.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 2

            pass

        def draw(self):
            if self.charain.f_dir == -1:
                self.charain.images['Run'][int(self.charain.frame)].draw(self.charain.x, self.charain.y, 100, 120)
            else:
                self.charain.images['Run'][int(self.charain.frame)].composite_draw(0, 'h', self.charain.x, self.charain.y,100, 120)


class Idle:
    def __init__(self, charain):
        self.charain = charain


    def enter(self,e):
        if event_stop(e):
            self.charain.f_dir = e[1]
        pass

    def exit(self,e):
        if e_down(e):
            self.charain.throw_cookie()
        pass

    def do(self):
        self.charain.frame = (self.charain.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 2
        pass

    def draw(self):
        if self.charain.f_dir == -1:
            self.charain.images['Idle'][int(self.charain.frame)].draw(self.charain.x, self.charain.y, 100, 120)
        else:
            self.charain.images['Idle'][int(self.charain.frame)].composite_draw(0, 'h',self.charain.x, self.charain.y, 100, 120)
        pass

class Charain:
    images = None
    def __init__(self,x,y):
        self.load_images()
        self.hp = 0
        self.x, self.y = x,y
        self.x_dir = 0
        self.y_dir = 0
        self.f_dir = 1
        self.frame = 0
        self.cookie_count = 0
        self.speed_boost = False
        self.speed_boost_time = 0
        self.damage_a = False
        self.damage_time = 0
        self.load_time = get_time()

        game_world.add_collision_pair('player:attack', self, None)
        game_world.add_collision_pair('player:cookie', self, None)
        game_world.add_collision_pair('player:item', self, None)

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
            self.WATTACK : {time_out: self.IDLE},
            self.TOUCH : { event_stop : self.IDLE}

            }
        )
        pass

    def load_images(self):
        if Charain.images == None:
            Charain.images = {}
            for name in rain_animation_names:
                Charain.images[name] = [load_image("./Cha_rain/" + name + " (%d)" % i + ".png") for i in range(1, 3)]


    def update(self):
        self.state_machine.update()
        if get_time() - self.load_time > 2 and self.cookie_count < 4:
            self.cookie_count += 1
            self.load_time = get_time()
        if self.hp <= 0:
            self.hp = 0
        game_data.player1_hp = self.hp
        if self.speed_boost and (get_time() - self.speed_boost_time) > 10:
            self.speed_boost = False
        if self.damage_a and (get_time() - self.damage_time) > 100:
            self.damage_a = False

        self.x = clamp(20 , self.x , 1460)
        self.y = clamp(20 , self.y , 1030)

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
                        self.state_machine.handle_state_event(('RUN', self.f_dir))
        else:
            self.state_machine.handle_state_event(('INPUT', event))

    def throw_cookie(self):
        if self.cookie_count > 0:
            cookie = Cookie(self.x, self.y, self.f_dir * 25, self.f_dir, self)
            game_world.add_object(cookie, 1)
            #game_world.add_collision_pair('player:cookie', None, cookie)
            self.cookie_count -= 1

    def attack(self):
        attack = Attack(self.x, self.y, self.f_dir, self)
        game_world.add_object(attack,1)

    def speed_booster(self):
        self.speed_boost = True
        self.speed_boost_time = get_time()


    def damage_plus(self):
        self.damage_a = True
        self.damage_time = get_time()
        pass


    def get_bb(self):
        return self.x - 35, self.y - 60, self.x + 35, self.y + 40

    def handle_collision(self, group, other):
        if group == 'player:cookie':
            damage = 10
            if other.owner.damage_a:
                damage = 20
            self.hp += damage
            print('cat hp + 10')
            self.state_machine.handle_state_event(('TOUCH', self.f_dir))
        if group == 'player:item':
            if other.effect == 'heal':
                self.hp -= 15
            elif other.effect == 'speed':
                self.speed_booster()
            elif other.effect == 'damage':
                self.damage_plus()
                pass
        if group == 'player:attack':
            damage = 10
            if other.owner.damage_a:
                damage = 20
            self.hp += damage
            print('cat hp + 10')
            self.state_machine.handle_state_event(('TOUCH', self.f_dir))

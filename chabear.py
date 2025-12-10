from pico2d import *
from sdl2 import *
from state_machine import StateMachine
from cookie import Cookie
from attack import Attack
from bear_attack import Bearattack
import game_world
import game_framework
import game_data


PIXEL_PER_METER = (1.0 / 0.03)  # 10픽셀 30센치미터
RUN_SPEED_KMPH = 50.0  # 시속 20킬로미터
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0) # 분속
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)        # 초속
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  #달리기 픽셀 속도


TIME_PER_ACTION = 1.0         #1초 액션 당 걸리는 시간
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_IDLE = 3
FRAMES_PER_TOUCH = 5

bear_animation_names = {'Idle':2 , 'Run':2 , 'Touch' : 2}

time_out = lambda e: e[0] == 'TIMEOUT'

def event_stop(e):
    return e[0] == 'STOP'

def event_run(e):
    return e[0] == 'RUN'

def q_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_q

def e_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_e

def r_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_r

def event_touch(e):
    return e[0] == 'TOUCH'

class Touch:
    def __init__(self, chabear):

        self.chabear = chabear
        self.time =0

    def enter(self, e):
        self.time = get_time()

    def exit(self,e):
        pass

    def do(self):
        self.chabear.frame = (self.chabear.frame + FRAMES_PER_TOUCH * ACTION_PER_TIME * game_framework.frame_time) % 2
        if get_time() - self.time >= 1:
            self.chabear.state_machine.handle_state_event(('STOP', self.chabear.f_dir))
        pass

    def draw(self):
        if self.chabear.f_dir == -1:
            self.chabear.images['Touch'][1].draw(self.chabear.x, self.chabear.y, 100, 120)
        else:
            self.chabear.images['Touch'][1].composite_draw(0,'h', self.chabear.x, self.chabear.y, 100, 120)

class WAttack:
        def __init__(self, chabear):
            self.chabear = chabear
            self.timer = 0

        def enter(self, e):
            if self.chabear.x_dir != 0:
                self.chabear.f_dir = self.chabear.x_dir

            self.timer = get_time()
            self.chabear.attack()

        def exit(self, e):
            pass

        def do(self):
            # self.chabear.x += self.chabear.x_dir * RUN_SPEED_PPS * game_framework.frame_time
            # self.chabear.y += self.chabear.y_dir * RUN_SPEED_PPS * game_framework.frame_time
            self.chabear.frame = (self.chabear.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 2

            if get_time() - self.timer >= 0.5:
                self.chabear.state_machine.handle_state_event(('TIMEOUT', self.chabear.f_dir))

        def draw(self):
            if self.chabear.f_dir == -1:
                self.chabear.images['Run'][1].draw(self.chabear.x, self.chabear.y, 100, 120)
            else:
                self.chabear.images['Run'][1].composite_draw(0, 'h', self.chabear.x, self.chabear.y, 100, 120)
            pass

class Battack:
    def __init__(self, chabear):
        self.chabear = chabear
        self.timer = 0

    def enter(self, e):
        if self.chabear.x_dir != 0:
            self.chabear.f_dir = self.chabear.x_dir
        self.timer = get_time()
        self.chabear.bear_attack()

    def exit(self, e):
        pass

    def do(self):
        if get_time() - self.timer >= 0.5:
            self.chabear.state_machine.handle_state_event(('TIMEOUT', self.chabear.f_dir))

        self.chabear.frame = (self.chabear.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 2

    def draw(self):
        if self.chabear.f_dir == -1:
            self.chabear.images['Run'][1].draw(self.chabear.x, self.chabear.y, 100, 120)
        else:
            self.chabear.images['Run'][1].composite_draw(0, 'h', self.chabear.x, self.chabear.y, 100, 120)
        pass


class Run:
    def __init__(self, chabear):
        self.chabear = chabear

    def enter(self,e):
        pass


    def exit(self,e):
        if e_down(e):
            self.chabear.throw_cookie()
        pass

    def do(self):
        speed = RUN_SPEED_PPS

        if self.chabear.speed_boost:
            speed *= 2
        if self.chabear.x_dir != 0:
            self.chabear.f_dir = self.chabear.x_dir
        self.chabear.x += self.chabear.x_dir * speed * game_framework.frame_time
        self.chabear.y += self.chabear.y_dir * speed * game_framework.frame_time
        self.chabear.frame = (self.chabear.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 2
        pass

    def draw(self):
        if self.chabear.f_dir == -1:
            self.chabear.images['Run'][int(self.chabear.frame)].draw(self.chabear.x, self.chabear.y, 100, 120)
        else:
            self.chabear.images['Run'][int(self.chabear.frame)].composite_draw(0, 'h', self.chabear.x, self.chabear.y, 100, 120)


class Idle:
    def __init__(self, chabear):
        self.chabear = chabear
    def enter(self,e):
        if event_stop(e):
            self.chabear.f_dir = e[1]

    def exit(self,e):
        if e_down(e):
            self.chabear.throw_cookie()
        pass

    def do(self):
        self.chabear.frame = (self.chabear.frame + FRAMES_PER_IDLE * ACTION_PER_TIME * game_framework.frame_time) % 2
        pass

    def draw(self):
        if self.chabear.f_dir == -1:
            self.chabear.images['Idle'][int(self.chabear.frame)].draw(self.chabear.x, self.chabear.y, 100, 120)
        else:
            self.chabear.images['Idle'][int(self.chabear.frame)].composite_draw(0, 'h', self.chabear.x, self.chabear.y, 100, 120)


class Chabear:
    images = None
    def __init__(self,x,y):
        self.hp_bar = load_image('hp_bar.png')
        self.attack_c = load_image('s_count.png')
        self.attack_count = 2
        self.count_time = get_time()
        self.hp = 0
        self.load_images()
        self.x, self.y = x, y
        self.x_dir = 0
        self.y_dir = 0
        self.f_dir = -1
        self.frame = 0
        self.speed_boost = False
        self.speed_boost_time = 0
        self.damage_a = False
        self.damage_time = 0
        self.load_time = get_time()
        self.cookie_count = 0

        game_world.add_collision_pair('player:rattack', self, None)
        game_world.add_collision_pair('player:cattack', self, None)
        game_world.add_collision_pair('player:attack', self, None)
        game_world.add_collision_pair('player:cookie', self, None)
        game_world.add_collision_pair('player:item', self, None)

        self.font = load_font('ENCR10B.TTF', 16)
        self.RUN = Run(self)
        self.IDLE = Idle(self)
        self.WATTACK = WAttack(self)
        self.TOUCH = Touch(self)
        self.BATTACK = Battack(self)

        self.state_machine = StateMachine(
            self.IDLE,               #시작 state
        {

                self.IDLE: {event_touch: self.TOUCH, e_down: self.IDLE, q_down: self.WATTACK,event_run: self.RUN, r_down: self.BATTACK},
                self.RUN: {event_touch: self.TOUCH, e_down: self.RUN, q_down: self.WATTACK,event_stop: self.IDLE,r_down: self.BATTACK},
                self.WATTACK : { time_out : self.IDLE},
                self.BATTACK: {time_out: self.IDLE},
                self.TOUCH : { event_stop : self.IDLE}
            }
        )

    def load_images(self):
        if Chabear.images == None:
            Chabear.images = {}
            for name, count in bear_animation_names.items():
                Chabear.images[name] = [
                    load_image(f"./Cha_bear/{name} ({i}).png") for i in range(1, count + 1)
                ]
            # for name in bear_animation_names:
            #     Chabear.images[name] = [load_image("./Cha_bear/" + name + " (%d)" % i + ".png") for i in range(1, 4)]


    def update(self):
        self.state_machine.update()
        if get_time() - self.load_time > 2 and self.cookie_count < 4:
            self.cookie_count += 1
            self.load_time = get_time()
        if get_time() - self.count_time > 30 and self.attack_count <2:
            self.attack_count +=1
            self.count_time = get_time()
        if self.hp >= 100:
            self.hp = 100
        game_data.player2_hp = self.hp
        if self.speed_boost and (get_time() - self.speed_boost_time) > 10:
            self.speed_boost = False
        if self.damage_a and (get_time() - self.damage_time) > 10:
            self.damage_a = False

        self.x = clamp(20 , self.x , 1460)
        self.y = clamp(20 , self.y , 1030)

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

    def draw(self):
        self.state_machine.draw()
        self.hp_bar.draw(self.x, self.y - 70, 1*self.hp, 20)
        if self.attack_count >= 1:
            self.attack_c.draw(self.x - 20, self.y + 60, 20, 20)
            if self.attack_count ==2:
                self.attack_c.draw(self.x + 20, self.y + 60, 20, 20)

    def get_bb(self):
        return self.x - 35, self.y - 60, self.x + 35, self.y + 40


    def throw_cookie(self):
        if self.cookie_count >0:
            cookie = Cookie(self.x, self.y, self.f_dir * 25, self.f_dir, self)
            game_world.add_object(cookie, 1)
            self.cookie_count -= 1

    def attack(self):
        attack = Attack(self.x, self.y, self.f_dir, self)
        game_world.add_object(attack,1)

    def bear_attack(self):
        bear_attack = Bearattack(self.x, self.y, self.f_dir, self)
        game_world.add_object(bear_attack, 1)
        self.attack_count -= 1

    def speed_booster(self):
        self.speed_boost = True
        self.speed_boost_time = get_time()

    def damage_plus(self):
        self.damage_a = True
        self.damage_time = get_time()
        pass


    def handle_collision(self, group, other):
        if group == 'player:cookie':
            damage = 10
            if other.owner.damage_a:
                damage = 20
            self.hp += damage
            print('bear hp + 10')
            self.state_machine.handle_state_event(('TOUCH', self.f_dir))

        if group == 'player:item':
            if other.effect == 'heal':
                self.hp -= 15
            elif other.effect == 'speed':
                self.speed_booster()
            elif other.effect == 'damage':
                self.damage_plus()

        if group == 'player:attack':
            damage = 10
            if other.owner.damage_a:
                damage = 20
            self.hp += damage
            print('cat hp + 10')
            self.state_machine.handle_state_event(('TOUCH', self.f_dir))

        if group == 'player:cattack':
            damage = 30
            if other.owner.damage_a:
                damage = 40
            self.hp += damage
            print('cat hp + 10')
            self.state_machine.handle_state_event(('TOUCH', self.f_dir))

        if group == 'player:rattack':
            damage = 12
            if other.owner.damage_a:
                damage = 18
            self.hp += damage
            print('cat hp + 10')
            self.state_machine.handle_state_event(('TOUCH', self.f_dir))
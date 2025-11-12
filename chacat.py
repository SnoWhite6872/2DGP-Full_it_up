from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_w, SDLK_a, SDLK_s, SDLK_d, SDLK_q
from state_machine import StateMachine


def event_stop(e):
    return e[0] == 'STOP'

def event_run(e):
    return e[0] == 'RUN'

def q_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_q #1p 약공격


# class WAttack:
#     def __init__(self, chacat):
#         self.chacat = chacat
#
#     def enter(self,e):
#         if q_down(e):
#             print("1P 공격")
#
#     def exit(self,e):
#         pass
#
#     def do(self):
#         pass
#
#     def draw(self):
#         self.chacat.image.draw(self.chacat.x, self.chacat.y)
#         pass



class Run:
        def __init__(self, chacat):
            self.chacat = chacat

        def enter(self,e):
            if self.chacat.x_dir != 0:
                self.chacat.f_dir = self.chacat.x_dir

        def exit(self,e):
            pass

        def do(self):
            self.chacat.x += self.chacat.x_dir * 1
            self.chacat.y += self.chacat.y_dir * 1
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
        self.x_dir = 0
        self.y_dir = 0
        self.f_dir = 1

        self.RUN = Run(self)
        self.IDLE = Idle(self)
        #self.WATTACK = WAttack(self)

        self.state_machine = StateMachine(
            self.IDLE,
        {
            self.IDLE: {event_run : self.RUN},
            self.RUN: {event_stop : self.IDLE},

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
from pico2d import *
import game_framework
import game_world
from random import randint

PIXEL_PER_METER = (1.0 / 0.03)
GRAVITY = 1
class Catattack:
    image = None

    def __init__(self, x, y, dir=0, owner = None):

        if Catattack.image is None:
            Catattack.image = load_image('Attack_cat.png')
        self.cur_y = y
        self.x = x + 200*dir
        self.y = y + 300
        self.v = 0
        self.timer = get_time()
        self.owner = owner
        game_world.add_collision_pair('player:cattack', None, self)

    def draw(self):
        self.image.draw(self.x, self.y, 200, 200)
        #draw_rectangle(*self.get_bb())

    def update(self):
        self.v += GRAVITY * PIXEL_PER_METER * game_framework.frame_time

        self.y -= 10* self.v * PIXEL_PER_METER * game_framework.frame_time

        if self.y <= self.cur_y:
            self.y = self.cur_y

        if get_time() - self.timer > 1:
            game_world.remove_object(self)

        pass


    def get_bb(self):
        return self.x - 100, self.y - 100, self.x + 100, self.y + 100

    def handle_collision(self, group, other):
        if group == 'player:cattack':
            game_world.remove_collision_object(self)


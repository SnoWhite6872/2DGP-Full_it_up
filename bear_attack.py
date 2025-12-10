from pico2d import *
import game_framework
import game_world
from random import randint

PIXEL_PER_METER = (1.0 / 0.03)
GRAVITY = 1
class Bearattack:
    image = None

    def __init__(self, x, y, dir=0, owner = None):
        self.dir = dir
        if Bearattack.image is None:
            Bearattack.image = load_image('Attack_bear.png')
        self.x = x + 200*dir
        self.y = y
        self.v = 0
        self.timer = get_time()
        self.owner = owner
        game_world.add_collision_pair('player:battack', None, self)

    def draw(self):
        if self.dir == 1:
            self.image.draw(self.x, self.y, 200, 200)
        else:
            self.image.composite_draw(0, 'h', self.x, self.y, 200, 200)
        #draw_rectangle(*self.get_bb())

    def update(self):

        self.x += 10 * PIXEL_PER_METER * game_framework.frame_time * self.dir



        if self.x <= 0 or self.x >= 1480:
            game_world.remove_object(self)

        pass


    def get_bb(self):
        return self.x - 100, self.y - 100, self.x + 100, self.y + 100

    def handle_collision(self, group, other):
        if group == 'player:battack':
            game_world.remove_collision_object(self)


from pico2d import *
import game_framework
import game_world
from random import randint

PIXEL_PER_METER = (1.0 / 0.03)

class Rcookie:
    image_table = {'1': 'I_Cookie01.png', '2': 'I_Cookie02.png', '3': 'I_Cookie03.png'}

    def __init__(self, x, y, dir=0, owner = None):
        self.r = randint(1, 3)

        if self.image_table[str(self.r)]:
            self.image = load_image(Rcookie.image_table[str(self.r)])
        self.x = x + 60*dir
        self.dir = dir
        self.y = y
        self.speed = 25
        self.owner = owner
        self.timer = get_time()
        game_world.add_collision_pair('player:rattack', None, self)

    def draw(self):
        self.image.draw(self.x, self.y, 60, 60)
        draw_rectangle(*self.get_bb())

    def update(self):
        if get_time() - self.timer > 0.3:
            self.x += self.speed * game_framework.frame_time * PIXEL_PER_METER *self.dir

        if self.x <0 or self.x > 1480:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def handle_collision(self, group, other):
        if group == 'player:rattack':
            game_world.remove_object(self)


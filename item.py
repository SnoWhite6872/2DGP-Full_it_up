from pico2d import *
import game_framework
import game_world
import random

PIXEL_PER_METER = (1.0 / 0.03)

class Icetea:
    image = None

    def __init__(self, x=random.randint(0, 1400), y=random.randint(0, 1000)):
        if Icetea.image == None:
            Icetea.image = load_image('I_Ice01.png')
        self.x = x
        self.y = y


    def draw(self):
        self.image.draw(self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())

    def update(self):
        # self.x += self.speed * game_framework.frame_time * PIXEL_PER_METER
        #
        # if self.x <0 or self.x > 1480:
        #     game_world.remove_object(self)
        pass

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'player:icetea':
            game_world.remove_object(self)


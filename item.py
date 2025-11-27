from pico2d import *
import game_framework
import game_world
import random

PIXEL_PER_METER = (1.0 / 0.03)

class Item:
    image_table = {'heal':'I_Ice01.png'}

    def __init__(self, effect,x=random.randint(0, 1400), y=random.randint(0, 1000)):
        self.effect = effect

        if self.image_table[effect]:
            self.image = load_image(Item.image_table[effect])

        self.x = x
        self.y = y
        game_world.add_collision_pair('player:item', None, self)


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
        if group == 'player:item':
            game_world.remove_object(self)


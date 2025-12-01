from pico2d import *
import game_framework
import game_world
import random
import game_data

PIXEL_PER_METER = (1.0 / 0.03)

class Item:
    image_table = {'heal':'I_Ice01.png', 'speed': 'I_pack_milktea.png', 'damage': 'I_syrup_sugar.png'}

    def __init__(self, effect, x = None, y = None):
        self.effect = effect
        self.y_dir = 1

        if self.image_table[effect]:
            self.image = load_image(Item.image_table[effect])
        if x is None:
            x = random.randint(0,1480)
        if y is None:
            y = random.randint(0,1050)

        self.x = x
        self.y = y
        self.set_y = y
        game_world.add_collision_pair('player:item', None, self)


    def draw(self):
        self.image.draw(self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())

    def update(self):
        # self.x += self.speed * game_framework.frame_time * PIXEL_PER_METER
        #
        # if self.x <0 or self.x > 1480:
        #     game_world.remove_object(self)

        if (self.set_y - self.y) <= -8:
            self.y_dir = -1
        elif (self.set_y - self.y) >= 8:
            self.y_dir = 1

        if self.y_dir == 1:
            self.y += self.y_dir * game_data.FRAMES_PER_TOUCH * game_framework.frame_time
        elif self.y_dir == -1:
            self.y += self.y_dir * game_data.FRAMES_PER_TOUCH * game_framework.frame_time


    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'player:item':
            game_world.remove_object(self)


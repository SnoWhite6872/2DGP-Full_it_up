from pico2d import *
import game_framework
import game_world
from random import randint

PIXEL_PER_METER = (1.0 / 0.03)
class Attack:
    image_table = {'0': 'attack_Cake02_Choco.png', '1': 'attack_Doughnut01.png', '2': 'attack_Ice_Vanilla.png'}

    def __init__(self, x, y, dir=0, owner = None):
        self.r = randint(0, 2)

        if self.image_table[str(self.r)]:
            self.image = load_image(Attack.image_table[str(self.r)])
        self.x = x + 100*dir
        self.y = y
        self.timer = get_time()
        self.owner = owner
        game_world.add_collision_pair('player:attack', None, self)

    def draw(self):
        self.image.draw(self.x, self.y, 100, 100)
        #draw_rectangle(*self.get_bb())

    def update(self):

        if get_time() - self.timer > 0.2:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 40

    def handle_collision(self, group, other):
        if group == 'player:attack':
            game_world.remove_collision_object(self)


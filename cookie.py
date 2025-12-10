from pico2d import *
import game_framework
import game_world

PIXEL_PER_METER = (1.0 / 0.03)
class Cookie:
    image = None

    def __init__(self, x, y, speed=25, dir=0, owner = None):
        if Cookie.image == None:
            Cookie.image = load_image('I_Cookie03.png')
        self.x = x + 60*dir
        self.y = y
        self.speed = speed
        self.owner = owner
        game_world.add_collision_pair('player:cookie', None, self)

    def draw(self):
        self.image.draw(self.x, self.y, 50, 50)
        #draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.speed * game_framework.frame_time * PIXEL_PER_METER

        if self.x <0 or self.x > 1480:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'player:cookie':
            game_world.remove_object(self)


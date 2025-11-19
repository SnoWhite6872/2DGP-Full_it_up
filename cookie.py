from pico2d import *
import game_framework
import game_world

PIXEL_PER_METER = (1.0 / 0.03)
class Cookie:
    image = None

    def __init__(self, x, y, speed = 15):
        if Cookie.image == None:
            Cookie.image = load_image('I_Cookie03.png')
        self.x = x
        self.y = y
        self.speed = speed

    def draw(self):
        self.image.draw(self.x, self.y, 50, 50)

    def update(self):
        self.x += self.speed * game_framework.frame_time * PIXEL_PER_METER

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def handle_collision(self, group, other):
        if group == 'chabear:cookie' or group == 'chacat:cookie':
            game_world.remove_object(self)


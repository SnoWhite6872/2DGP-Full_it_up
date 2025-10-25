from pico2d import *

from chabear import Chabear

class BGbasic:
    def __init__(self):
        self.image = load_image('BG_basic.png')
    def draw(self):
        self.image.draw(1440/2, 3120/2)
    def update(self):
        pass


open_canvas(1440, 2000)
running = True


def handle_events():
    global running
    pass

def reset_world():
    global chabear
    global world
    global bgbasic
    world = []

    bgbasic = BGbasic()
    world.append(bgbasic)
    chabear = Chabear()
    world.append(chabear)

    pass




def update_world():
    for o in world:
        o.update()


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()



reset_world()

while running:
    handle_events()
    update_world()
    render_world()

    delay(0.05)
close_canvas()
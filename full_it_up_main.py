from pico2d import *

from chabear import Cha_bear

open_canvas()
running = True


def handle_events():
    global running
    pass

def reset_world():
    global chabear
    chabear = Cha_bear()
    pass




def update_world():
    pass


def render_world():
    pass



reset_world()

while running:
    handle_events()
    update_world()
    render_world()

    delay(0.05)
close_canvas()
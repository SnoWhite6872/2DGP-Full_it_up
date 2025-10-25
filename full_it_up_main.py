from pico2d import *

from chabear import Chabear

open_canvas()
running = True


def handle_events():
    global running
    pass

def reset_world():
    global chabear
    global world

    world = []
    chabear = Chabear()
    world.append(chabear)
    pass




def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.update()
    update_canvas()
    pass



reset_world()

while running:
    handle_events()
    update_world()
    render_world()

    delay(0.05)
close_canvas()
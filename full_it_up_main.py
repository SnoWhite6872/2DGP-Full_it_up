from pico2d import *

from bgbasic import BGbasic
from chabear import Chabear
from chacat import Chacat

open_canvas(504, 1050)
running = True


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            chabear.handle_event(event)
            chacat.handle_event(event)
    pass

def reset_world():
    global chabear
    global chacat
    global world
    global bgbasic
    world = []

    bgbasic = BGbasic()
    world.append(bgbasic)
    chabear = Chabear()
    world.append(chabear)
    chacat = Chacat()
    world.append(chacat)

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
from pico2d import *

import game_world
from bgbasic import BGbasic
from chabear import Chabear
from chacat import Chacat




def handle_events():
    global running

    event_list = get_events()

    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            chabear.handle_event(event)
            chacat.handle_event(event)
    pass

def init():
    global chabear
    global chacat
    global bgbasic

    bgbasic = BGbasic()
    game_world.add_object(bgbasic, 0)
    chabear = Chabear()
    game_world.add_object(chabear, 1)
    chacat = Chacat()
    game_world.add_object(chacat, 1)

    pass




def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

running = True



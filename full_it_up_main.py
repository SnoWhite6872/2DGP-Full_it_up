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

def reset_world():
    global chabear
    global chacat
    global bgbasic

    bgbasic = BGbasic()
    game_world.add_object(bgbasic)
    chabear = Chabear()
    game_world.add_object(chabear)
    chacat = Chacat()
    game_world.add_object(chacat)

    pass




def update_world():
    game_world.update()


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

running = True
open_canvas(504, 1050)

reset_world()

while running:
    handle_events()
    update_world()
    render_world()

    delay(0.01)
close_canvas()
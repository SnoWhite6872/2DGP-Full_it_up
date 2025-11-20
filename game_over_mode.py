from pico2d import *
import game_framework
import select_mod

image = None

def init():
    global image
    image = load_image('game_over.png')
    pass

def finish():
    global image
    del image
    pass

def update():
    pass

def draw():
    global image
    clear_canvas()
    image.draw(1480//2, 1050//2,100,100)
    update_canvas()
    pass

def handle_events():
    event_list = get_events()

    for event in event_list:
        if event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            game_framework.change_mode(select_mod)

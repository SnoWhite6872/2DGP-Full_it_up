from pico2d import *
import game_framework
import full_it_up_main

image0 = None
image1 = None
image2 = None

def init():
    global image0, image1
    image0 = load_image('BG_basic.png')
    image1 = load_image('BG_luxury.png')
    pass

def finish():
    global image0, image1
    del image0, image1
    pass

def update():
    pass

def draw():
    pass

def handle_events():
    event_list = get_events()  # 버퍼로부터 모든 입력을 갖고 온다.
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(full_it_up_main)
        elif event.type == SDL_MOUSEMOTION:
            pass
    pass
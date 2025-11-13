from pico2d import *
import game_framework
import full_it_up_main

image = None

def init():
    global image
    image = load_image('spare_title.png')

def finish():
    global image
    del image
    pass


def update():
    pass

def draw():
    clear_canvas()
    image.draw(1480//2, 1050//2)
    update_canvas()
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
    pass
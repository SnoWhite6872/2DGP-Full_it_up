from pico2d import *
import game_framework
import full_it_up_main
import game_data

image0 = None
image1 = None
image2 = None
cc = None
cb = None

def init():
    global map, image0, image1, cc, cb
    map = 0
    image0 = load_image('BG_basic.png')
    image1 = load_image('BG_luxury.png')
    cc = load_image('Cha_cat.png')
    cb = load_image('Cha_bear.png')
    pass

def finish():
    global image0, image1
    del image0, image1
    pass

def update():
    pass

def draw():
    global map
    clear_canvas()
    if map == 0:
        image0.draw(1480//2, 1050//2)
    elif map == 1:
        image1.draw(1480//2, 1050//2)
    update_canvas()
    pass

def handle_events():
    global map
    event_list = get_events()  # 버퍼로부터 모든 입력을 갖고 온다.
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_data.select_mod = map
            game_framework.change_mode(full_it_up_main)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            map = (map + 1 ) % 2
    pass
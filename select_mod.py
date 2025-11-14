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
    global map, image0, image1, cc, cb, player1, player2
    player1 = 0
    player2 = 0
    map = 0
    image0 = load_image('BG_basic.png')
    image1 = load_image('BG_luxury.png')
    cc = load_image('Cha_cat.png')
    cb = load_image('Cha_bear.png')
    pass

def finish():
    global image0, image1, cc, cb
    del image0, image1, cc, cb
    pass

def update():
    pass

def draw():
    global map, player1, player2
    clear_canvas()
    if map == 0:
        image0.draw(1480//2, 1050//2)
    elif map == 1:
        image1.draw(1480//2, 1050//2)

    if player1 == 0:
        cc.draw(100, 700)
    elif player1 == 1:
        cb.draw(100, 700)

    if player2 == 0:
        cc.draw(1380, 700)
    elif player2 == 1:
        cb.draw(1380, 700)

    update_canvas()
    pass

def handle_events():
    global map, player1, player2
    event_list = get_events()  # 버퍼로부터 모든 입력을 갖고 온다.
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            map = (map + 1 ) % 2
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            if event.key == SDLK_d:
                player1 = (player1 + 1) % 2
            if event.key == SDLK_a:
                if player1 == 0:
                    player1 = 1
                else:
                    player1 = (player1 - 1) % 2
            if event.key == SDLK_RIGHT:
                player2 = (player2 + 1) % 2
            if event.key == SDLK_LEFT:
                if player2 == 0:
                    player2 = 1
                else:
                    player2 = (player2 - 1) % 2
            if event.key == SDLK_SPACE:
                game_data.select_mod = map
                game_data.player_1 = player1
                game_data.player_2 = player2
                game_framework.change_mode(full_it_up_main)

    pass
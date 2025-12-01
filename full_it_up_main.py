from pico2d import *

import game_world
from bgbasic import BGbasic
from chabear import Chabear
from chacat import Chacat
from bgluxury import BGluxury
from item import Item
from random import choice
import game_data
import select_mod
from player_one import PlayerOne
from player_two import PlayerTwo

import game_framework

timer = get_time()

def handle_events():

    event_list = get_events()

    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif game_data.game_end == 1 and event.type == SDL_KEYDOWN and event.key ==SDLK_SPACE:
            game_framework.change_mode(select_mod)
        else:
            p1.handle_event(event)
            p2.handle_event(event)
    pass

def init():
    global chabear, chacat
    global image_gameover
    global char1, char2, p1, p2

    Cha = [Chacat, Chabear]

    char1 = Cha[game_data.player_1](game_data.player1_x, game_data.player1_y)
    char2 = Cha[game_data.player_2](game_data.player2_x, game_data.player2_y)

    p1 = PlayerOne(char1)
    p2 = PlayerTwo(char2)

    image_gameover = load_image('game_over.png')
    bgbasic = BGbasic()
    bgluxury = BGluxury()
    if game_data.select_mod == 0:
        game_world.add_object(bgbasic, 0)
    elif game_data.select_mod == 1:
        game_world.add_object(bgluxury, 0)


    #캐릭터 오브젝트 추가
    game_world.add_object(char1, 1)
    game_world.add_object(char2, 1)


    #충돌 관리
    game_world.add_collision_pair('player:player', char1, None)
    game_world.add_collision_pair('player:player', char2, None)
    #game_world.add_collision_pair('chacat:icetea', None, ice_tea)


    pass

def spawn_item():
    global timer

    item_effects = ['heal', 'speed', 'damage']
    if get_time() - timer > 2:
        item_random = choice(item_effects)
        item = Item(item_random)
        game_world.add_object(item, 1)

        timer = get_time()



def update():
    global image_gameover
    game_world.update()
    game_world.handle_collision()
    spawn_item()

    if game_data.player1_hp >= 100 or game_data.player2_hp >= 100:
        game_data.game_end = 1

    # if game_data.player1_hp >= 100 or game_data.player2_hp >=100:
    #     # game_framework.push_mode(game_over_mode)
    #     image_gameover.draw(1480//2, 1050//2,100,100)


def draw():
    clear_canvas()
    game_world.render()
    if game_data.player1_hp >= 100 or game_data.player2_hp >=100:
        # game_framework.push_mode(game_over_mode)
        image_gameover.draw(1480//2, 800, 1000, 200)
    update_canvas()

def finish():
    game_world.clear()
    pass

def pause():
    pass
def resume():
    pass
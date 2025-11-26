from pico2d import *

import game_world
from bgbasic import BGbasic
from chabear import Chabear
from chacat import Chacat
from bgluxury import BGluxury
from item import Icetea
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
            chabear.handle_event(event)
            chacat.handle_event(event)
    pass

def init():
    global chabear
    global chacat
    global bgbasic
    global image_gameover
    global ice_tea
    global char1, char2

    Cha = [Chacat, Chabear]

    char1 = Cha[game_data.player_1]()
    char2 = Cha[game_data.player_2]()

    image_gameover = load_image('game_over.png')
    bgbasic = BGbasic()
    bgluxury = BGluxury()
    if game_data.select_mod == 0:
        game_world.add_object(bgbasic, 0)
    elif game_data.select_mod == 1:
        game_world.add_object(bgluxury, 0)

    # chabear = Chabear()
    # game_world.add_object(chabear, 1)
    # chacat = Chacat()
    # game_world.add_object(chacat, 1)
    ice_tea = Icetea(1480//2, 1050//2)
    game_world.add_object(ice_tea)
    game_world.add_collision_pair('chabear:icetea', None, ice_tea)
    game_world.add_collision_pair('chacat:icetea', None, ice_tea)


    pass

def spawn_item():
    global timer, ice_tea

    if get_time() - timer > 10:
        ice_tea = Icetea()
        game_world.add_object(ice_tea, 1)
        game_world.add_collision_pair('chabear:icetea', None, ice_tea)
        game_world.add_collision_pair('chacat:icetea', None, ice_tea)
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
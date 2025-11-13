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
    pass
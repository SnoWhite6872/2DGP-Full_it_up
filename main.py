from pico2d import *
import game_framework
import title_mode as start_mode  #처음 시작할 모드 정하기


open_canvas(1480, 1050)
game_framework.run(start_mode)
close_canvas()
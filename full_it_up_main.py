from pico2d import *



open_canvas()
running = True
while running:
    handle_events()
    update_world()
    draw_world()

    delay(0.05)
close_canvas()
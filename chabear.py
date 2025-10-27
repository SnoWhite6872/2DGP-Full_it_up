from pico2d import load_image
from sdl2 import SDL_KEYUP, SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN

class Run:
    def __init__(self, chabear):
        self.chabear = chabear
    def enter(self,e):
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_RIGHT:
                self.chabear.w_dir =1
            elif e.key == SDLK_LEFT:
                self.chabear.w_dir = -1
            elif e.key == SDLK_UP:
                self.chabear.h_dir = 1
            elif e.key == SDLK_DOWN:
                self.chabear.h_dir = -1
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_RIGHT or e.key == SDLK_LEFT:
                self.chabear.w_dir =0   #딕셔너리로 상태 변경시 수정 필요
            elif e.key == SDLK_UP or e.key ==SDLK_DOWN:
                self.chabear.h_dir =0

        pass
    def exit(self,e):
        pass
    def do(self):
        self.chabear.x += self.chabear.w_dir *5
        self.chabear.y += self.chabear.h_dir * 5
        pass
    def draw(self):
        self.chabear.image.draw(self.chabear.x, self.chabear.y)




class Chabear:
    def __init__(self):
        self.image = load_image('Cha_bear.png')
        self.x, self.y = 252, 525
        self.w_dir = 0
        self.h_dir = 0

        self.Run = Run(self)
        pass

    def update(self):
        self.Run.do()
        pass

    def draw(self):
        self.Run.draw()
        pass


    def handle_event(self, event):
        self.Run.enter(event)
        pass

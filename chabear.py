from pico2d import load_image
from sdl2 import SDL_KEYUP, SDL_KEYDOWN, SDLK_RIGHT, SDLK_LEFT

class Run:
    def __init__(self, chabear):
        self.chabear = chabear
    def enter(self,e):
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_RIGHT:
                self.chabear.dir =1
            elif e.key == SDLK_LEFT:
                self.chabear.dir = -1
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_RIGHT:
                self.chabear.dir = -1
            elif e.key == SDLK_LEFT:
                self.chabear.dir = 1
        pass
    def exit(self,e):
        pass
    def do(self):
        self.chabear.x += self.chabear.dir *10
        pass
    def draw(self):
        self.chabear.image.draw(self.chabear.x, self.chabear.y)




class Chabear:
    def __init__(self):
        self.image = load_image('Cha_bear.png')
        self.x, self.y = 252, 525
        self.dir = 0


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

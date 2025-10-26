from pico2d import load_image


class Run:
    def __init__(self, chabear):
        self.chabear = chabear
    def enter(self,e):
        pass
    def exit(self,e):
        pass
    def do(self):
        pass
    def draw(self):
        self.chabear.image.draw(self.chabear.x, self.chabear.y)




class Chabear:
    def __init__(self):
        self.image = load_image('Cha_bear.png')
        self.x, self.y = 252, 525
        self.Run = Run(self)
        pass
    def draw(self):
        pass
    def update(self):
        pass

    def handle_event(self, event):
        #self.Run
        pass

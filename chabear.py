from pico2d import load_image


class Chabear:
    def __init__(self):
        self.image = load_image('Cha_bear.png')
        pass
    def draw(self):
        self.image.draw(252, 300)
        pass
    def update(self):

        pass

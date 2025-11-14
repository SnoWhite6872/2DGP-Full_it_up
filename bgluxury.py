from pico2d import load_image


class BGluxury:
    def __init__(self):
        self.image = load_image('BG_luxury.png')
    def draw(self):
        self.image.draw(1480//2, 1050//2)
    def update(self):
        pass

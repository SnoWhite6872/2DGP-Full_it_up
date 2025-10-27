from pico2d import load_image
from state_machine import StateMachine

class Chacat:
    def __init__(self):
        self.image = load_image('Cha_cat.png')
        self.x, self.y = 300, 400

        #self.state_machine = StateMachine()
        pass


    def update(self):
        pass

    def draw(self):
        pass

    def handle_events(self, event):
        #self.state_machine.handle_state_event(event)
        pass
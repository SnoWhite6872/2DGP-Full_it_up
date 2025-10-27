class StateMachine:
    def __init__(self, start_state, rules):
        self.cur_state = start_state
        self.rules = rules
        self.cur_state.enter(('start', 0))
        pass

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()

    def handle_state_event(self, state_event):
        pass
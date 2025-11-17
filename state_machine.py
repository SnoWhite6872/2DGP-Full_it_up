from event_to_string import event_to_string
from sdl2 import SDLK_q, SDLK_m ,SDL_KEYDOWN
class StateMachine:
    def __init__(self, start_state, rules):
        self.cur_state = start_state
        self.rules = rules
        self.cur_state.enter(('start', 0))

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()

    def handle_state_event(self, state_event):
        # if state_event[1] == SDLK_q or state_event[1] == SDLK_m:
        #     for check_event in self.rules[self.cur_state].keys():
        #         if check_event(state_event):
        #             self.next_state = self.rules[self.cur_state][check_event]
        #             self.cur_state.exit(state_event)
        #             self.next_state.enter(state_event)
        #             self.next_state.exit(state_event)
        #             self.cur_state.enter(state_event)
        #             print(f'{self.cur_state.__class__.__name__} -----------{event_to_string(state_event)}----------> {self.cur_state.__class__.__name__}')
        #             return
        #
        #
        #
        # else:
            for check_event in self.rules[self.cur_state].keys():
                if check_event(state_event):
                    self.next_state = self.rules[self.cur_state][check_event]
                    self.cur_state.exit(state_event)
                    self.next_state.enter(state_event)
                    print(f'{self.cur_state.__class__.__name__} -----------{event_to_string(state_event)}----------> {self.next_state.__class__.__name__}')
                    self.cur_state = self.next_state
                    return
        #print(f'처리되지 않은 이벤트{event_to_string(state_event)}가 있습니다.')
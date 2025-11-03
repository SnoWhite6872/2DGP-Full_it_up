running = None
stack = None

def change_mode(mode):
    pass

def push_mode(mode):
    pass

def pop_mode():
    pass




def quit():
    global running
    running = False



def run(start_mode):
    global stack, running

    running = True
    stack = [start_mode]
    start_mode.init()

    while running:     #STACK에 있는 모드 실행
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

    while (len(stack) > 0):  #STACK에 모드가 남아 있다면 제거
        stack[-1].finish()
        stack.pop()
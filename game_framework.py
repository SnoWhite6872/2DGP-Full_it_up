running = None
stack = None

def change_mode(mode):
    global stack

    if (len(stack) > 0):  #이전 모드 제거
        stack[-1].finish()
        stack.pop()

    stack.append(mode)   #새 모드 실행
    mode.init()
    pass

def push_mode(mode):
    global stack

    if (len(stack) > 0):
        stack[-1].pause()   #이전 모드 일시정지

    stack.append(mode)   #추가한 모드 실행
    mode.init()
    pass

def pop_mode():
    global stack

    if (len(stack)> 0):
        stack[-1].finish()  #실행중인 모드 종료
        stack.pop()

    if (len(stack) > 0):
        stack[-1].resume()  #이전 모드 다시 시작
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
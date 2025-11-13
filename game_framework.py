import time

running = None
stack = None

frame_time = 0.0

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
    global stack, running, frame_time


    frame_time = 0.0
    current_time = time.time()  #프레임 시간을 재기 위한 현재 시간

    running = True
    stack = [start_mode]
    start_mode.init()

    while running:     #STACK에 있는 모드 실행
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

        frame_time = time.time() - current_time    #프레임 시간 계산
        current_time += frame_time   #다시 현재 시간으로 변경
        frame_rate = 1.0 / frame_time  #프레임 레이트 계산

    while (len(stack) > 0):  #STACK에 모드가 남아 있다면 제거
        stack[-1].finish()
        stack.pop()
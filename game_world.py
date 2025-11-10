#world에 layer을 추가하여 객체 속성에 따라 관리

world = [[],[]]

def add_object(o, l = 0):
    world[l].append(o)

def update():
    for layer in world:
        for o in layer:
            o.update()
def render():
    for layer in world:
        for o in layer:
            o.draw()


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return

def clear():
    for layer in world:
        layer.clear()


def collide(a,b): #충돌 체크 함수 a와 b의 충돌
    left_a, bottom_a, right_a, top_a = a.get_bb() #상하좌우 끝의 범위 전달
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


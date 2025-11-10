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

def remove_collision_object(o):
    pass

def remove_collision_group_in_object(group, o):
    pass

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
collision_pair = {}   #딕셔너리로 충돌 관리,

def add_collision_pair(group, a, b):        #group = 어떤 물체끼리의 작용인지 /
    if group not in collision_pair:  #없다면 새로 추가
        collision_pair[group] = [ [], [] ] #튜플속 리스트로 관리
    if a:
        collision_pair[group][0].append(a)
    if b:
        collision_pair[group][1].append(b)
    pass

def handle_collision():
    for group, pairs in collision_pair.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
    return None
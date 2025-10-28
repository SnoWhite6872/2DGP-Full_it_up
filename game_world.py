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
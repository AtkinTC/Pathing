import sys, pygame
from pygame.locals import *
from random import randint
import draw, pathing

nodes = {}
large = 0
size = w, h = 320,240

def build_n(x, y):
    global nodes
    global large
    id = 1
    while id in nodes.keys():
        id += 1
    node = {'id':id, 'loc': (x, y), 'links': set()}
    nodes[id] = node
    if id > large:
        large = id
    return id

def del_n(id):
    global nodes
    if id in nodes:
        for i in nodes.keys():
            nodes[i]['links'].discard(i)
        del nodes[id]
        return True
    return False

def connect_n(id1, id2):
    if id1 in nodes and id2 in nodes and id1 is not id2:
        nodes[id1]['links'].add(id2)
        nodes[id2]['links'].add(id1)
        return True
    return False
    
draw.init(w,h)

done = False
action = False
grabbed = 0
mode = 'new'
atoz = [None, None]
path = []
while not done:
    m_pos = mx, my = pygame.mouse.get_pos()

    path = []
    if atoz[0] and atoz[1]:
        path = pathing.a_star(nodes, atoz[0], atoz[1])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if not action:
                if event.unicode == 'm':
                    mode = 'move'
                elif event.unicode == 'l':
                    mode = 'link'
                elif event.unicode == 'n':
                    mode = 'new'
                elif event.unicode == 'a':
                    mode = 'first'
                elif event.unicode == 'z':
                    mode = 'last'
        if event.type == pygame.MOUSEBUTTONDOWN:
            def grab():
                for n in nodes:
                    x,y = nodes[n]['loc']
                    if abs(mx-x) < 5 and abs(my-y) < 5:
                        return n
                return None
                
            if mode == 'new':
                action = 'new'
            elif mode == 'link':
                grabbed = grab()
                if grabbed:
                    action = 'link'
            elif mode == 'move':
                grabbed = grab()
                if grabbed:
                    action = 'move'
            elif mode == 'first':
                atoz[0] = grab()
            elif mode == 'last':
                atoz[1] = grab()
                    
        if event.type == pygame.MOUSEBUTTONUP:
            if action == 'new':
                build_n(mx, my)
                action = False
            elif action == 'link':
                for n in nodes:
                    x,y = nodes[n]['loc']
                    if n != grabbed and abs(mx-x) < 5 and abs(my-y) < 5:
                        connect_n(n,grabbed)
                        break
                action = False
            elif action == 'move':
                action = False

    if action == 'move':
        nodes[grabbed]['loc'] = m_pos


    draw.draw_links(nodes, large)
    draw.draw_nodes(nodes, large)

    for i in range(len(path)-1):
        pos1 = nodes[path[i]]['loc']
        pos2 = nodes[path[i+1]]['loc']
        draw.draw_link(pos1, pos2, 0, 255, 100)

    if atoz[0]:
        draw.draw_node(nodes[atoz[0]]['loc'], 0, 255, 100)

    if atoz[1]:
        draw.draw_node(nodes[atoz[1]]['loc'], 0, 255, 100)

    if action == 'place':
        draw.draw_node(m_pos, 255, 100, 100)
    if action == 'link':
        draw.draw_link(nodes[grabbed]['loc'], m_pos, 255, 100, 100)

    for id in nodes:
        draw.draw_text(str(id), nodes[id]['loc'], 255, 255, 255)

    draw.draw_text('('+str(mx)+',', (0,0), 255, 255, 255)
    draw.draw_text(str(my)+')', (30,0), 255, 255, 255)
    draw.draw_text('mode:' + mode, (70,0), 255, 255, 255)
    draw.draw_text(str(atoz), (160,0), 255, 255, 255)
    
    draw.flip()
pygame.quit()

    


    

import sys, pygame
from pygame.locals import *
import pygame.font

nodes = {}
large = 0
size = w, h = 320,240


def build_n(x,y):
    global nodes
    global large
    id = 1
    while id in nodes.keys():
        id += 1
    node = {'id':id, 'loc':(x,y), 'links':set()}
    nodes[id] = node
    if id > large:
        large = id
    return id

def connect_n(id1, id2):
    if id1 in nodes and id2 in nodes and id1 is not id2:
        nodes[id1]['links'].add(id2)
        nodes[id2]['links'].add(id1)
        return True
    return False

def draw_nodes(screen):
    for i in [i for i in range(1, large+1) if i in nodes]:
        pygame.draw.circle(screen, (0,100,255), nodes[i]['loc'], 3)

def draw_links(screen):
    for i in [i for i in range(1, large+1) if i in nodes]:
        for j in nodes[i]['links']:
            if j > i:
                posi = nodes[i]['loc']
                posj = nodes[j]['loc']

                pygame.draw.line(screen, (0,100,255), posi, posj, 1)

build_n(30,30)

screen = pygame.display.set_mode(size)

pygame.font.init()
font = pygame.font.SysFont(None, 15)

done = False
action = False
grabbed = 0
mode = 'new'
while not done:
    m_pos = mx, my = pygame.mouse.get_pos()
    
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode == 'new':
                action = 'new'
            elif mode == 'link':
                for n in nodes:
                    x,y = nodes[n]['loc']
                    if abs(mx-x) < 5 and abs(my-y) < 5:
                        grabbed = n
                        action = 'link'
                        break
            elif mode == 'move':
                for n in nodes:
                    x,y = nodes[n]['loc']
                    if abs(mx-x) < 5 and abs(my-y) < 5:
                        grabbed = n
                        action = 'move'
                        break
                    
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

    screen.fill((0,0,0))

    draw_links(screen)
    draw_nodes(screen)

    if action == 'place':
        pygame.draw.circle(screen, (0,255,100), m_pos, 3)
    if action == 'link':
        pygame.draw.line(screen, (0,255,100), nodes[grabbed]['loc'], m_pos, 1)

    for id in nodes:
        tex_id = font.render(str(id), True, (255,255,255))
        screen.blit(tex_id, nodes[id]['loc'])
    
    tex_x = font.render('('+str(mx)+',', True, (255,255,255))
    tex_y = font.render(str(my)+')', True, (255,255,255))
    tex_mode = font.render('mode:' + mode, True, (255,255,255))
    screen.blit(tex_x, (0, 0))
    screen.blit(tex_y, (30, 0))
    screen.blit(tex_mode, (70, 0))
    pygame.display.flip()
pygame.quit()

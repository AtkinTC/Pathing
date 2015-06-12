import sys, pygame
from pygame.locals import *
import pygame.font

w, h = 320,240
screen = None
font = None

def init(width=320, height=240):
    global screen, w, h, font
    w = width
    h = height
    screen = pygame.display.set_mode((w,h))
    screen.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont(None, 15)
    
def draw_nodes(nodes, large):
    for i in [i for i in range(1, large+1) if i in nodes]:
        draw_node(nodes[i]['loc'], 0, 100, 255)

def draw_node(pos, r, g, b):
    pygame.draw.circle(screen, (r,g,b), pos, 3)

def draw_links(nodes, large):
    for i in [i for i in range(1, large+1) if i in nodes]:
        for j in nodes[i]['links']:
            if j > i:
                draw_link(nodes[i]['loc'], nodes[j]['loc'], 0, 100, 255)

def draw_link(pos1, pos2, r, g, b):
    pygame.draw.line(screen, (r,g,b), pos1, pos2, 1)

def draw_text(text, pos, r,g,b):
    text = font.render(text, True, (r,g,b))
    screen.blit(text, pos)

def flip(col = (0,0,0)):
    pygame.display.flip()
    screen.fill(col)

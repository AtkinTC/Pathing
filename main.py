"{'id':xxx, 'loc': (x,y), 'links': {xxx,xxx,xxx,...}}"

#A* pathfinding with lookup table

import sys, pygame
from pygame.locals import *
from random import randint
import time


def timeme(method):
    def wrapper(*args, **kw):
        startTime = time.time() * 1000
        result = method(*args, **kw)
        endTime = time.time() * 1000

        print (endTime-startTime, 'ms')
        return result
    return wrapper

nodes = {}
lookup = {}
large = 0

def init():
    global nodes
    global large
    global lookup
    nodes = {}
    lookup = {}
    large = 0

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

def print_connects():
    for i in [i for i in range(1, large+1) if i in nodes]:
        for j in nodes[i]['links']:
            if j > i:
                print i, ' --> ', j

def dist(id1, id2):
    return pyth(nodes[id1]['loc'], nodes[id2]['loc'])

def pyth(xy1, xy2):
    return pow(pow(xy2[0]-xy1[0],2) + pow(xy2[1]-xy1[1],2),0.5)

#@timeme
def a_star(start,end):
    global lookup
    closedset = []
    openset = [start]
    came_from = {}
    
    #g_score is the distance to in current best path
    g_score = {start : 0}
    #f_score is an estimate of the total distance through this node
    #f_score must be <= to the unknown real distance
    f_score = {start : g_score[start] + dist(start, end)}

    temp_end = end
    while len(openset) > 0:
        #print openset
        short = -1
        for k in openset:
            if short is -1 or f_score[k] < f_score[short]:
                short = k
        current = short
        #current becomes the temporary end node, if path is in the lookup
        if lookup.get(current, {}).get(temp_end, -1) is not -1:
            temp_end = current

        
        if current == temp_end:

            #if some best route for part of the path has been calculated
            #the lookup table is updated with that information
            if came_from is not {}:
                path = construct_path(came_from, temp_end)
                for i in range(len(path)-1):
                    if path[i] not in lookup:
                        lookup[path[i]] = {}
                    lookup[path[i]][end] = path[i+1]

            #by this point a complete path will be in the lookup table, if one is possible
            #generates a path from the lookup table entries
            t_current = start
            t_path = [t_current]
            while t_current != end:
                t_current = lookup[t_current][end]
                t_path.append(t_current)

            #adds the whole path to the lookup table
            #slows down lengthy searches to fill lookup table sooner
            for i in range(len(path)-1):
                if path[i] not in lookup:
                    lookup[path[i]] = {}
                for j in range(i, len(path)):
                    lookup[path[i]][path[j]] = path[i+1]
                    
            return t_path


        #current node is removed from the queue and marked complete
        openset.remove(current)
        closedset.append(current)
        
        for node in nodes[current]['links']:
            
            #skip this if the node is already in the closed set
            if node in closedset:
                continue

            #calculate a g_score for this potential route to node
            temp_g_score = g_score[current] + dist(current, node)

            #updates route information for this node if none exists or if the new route is better
            if node not in openset or temp_g_score < g_score[node]:
                came_from[node] = current
                g_score[node] = temp_g_score
                f_score[node] = g_score[node] + dist(node, end)
                if node not in openset:
                    openset.append(node)

    #fail state
    return [-1, end]

def construct_path(came_from, current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path



init()

d = 45
tot = 1000
build_n(1,1)
build_n(d,d)

used = [(1,1),(d,d)]
current = 3
for i in range(tot-2):
    x,y = (-1,-1)
    f = False
    while not f:
        x,y = (randint(1,d), randint(1,d))
        if (x,y) not in used:
            used.append((x,y))
            f = True
        #print x,y
    build_n(x,y)
    for j in range(1,current):
        if dist(current, j) < 2.5:
            connect_n(current,j)
    current += 1

for j in range(3,tot):
        if dist(1, j) < 4:
            connect_n(1,j)
for j in range(3,tot):
        if dist(2, j) < 4:
            connect_n(2,j)
    

pygame.init()

size = width, height = 640, 480

screen = pygame.display.set_mode(size)
w = 10
done = False

print large, ', ', len(nodes.keys())

step1 = 1
step2 = 1

#r = a_star(1,257)
#print r

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    #print step1, ', ', step2
    r = a_star(step1,step2)

    l_size = 0
    for k in lookup:
        for k2 in lookup[k]:
            l_size += 1

    print step1, ', ', step2, ', lookup size = ', l_size
    print len(r)
    if len(r) < 1: time.sleep(0.5)
    
    #print len(r)
    #print 'path   -> ', r
    #print 'lookup -> ', lookup
        
    step2 += 1
    if step2 >= large:
        step1 += 1
        step2 = 1
        if step1 >= large:
            done = True
    
    
    
    screen.fill((0,0,0))
   # pygame.draw.circle(screen, (255,255,255), (10,10), 10)

    scale = 10
    for i in [i for i in range(1, large+1) if i in nodes]:
        for j in nodes[i]['links']:
            if j > i:
                posi = (nodes[i]['loc'][0]*scale, nodes[i]['loc'][1]*scale)
                posj = (nodes[j]['loc'][0]*scale, nodes[j]['loc'][1]*scale)

                pygame.draw.line(screen, (0,100,255), posi, posj, 1)
                
    for k in nodes:
        pos = (nodes[k]['loc'][0]*scale, nodes[k]['loc'][1]*scale)
        pygame.draw.circle(screen, (0,100,255), pos, 2)

    for i in range(len(r)-1):
        if r[i] > 0:
            pos1 = (nodes[r[i]]['loc'][0]*scale, nodes[r[i]]['loc'][1]*scale)
            pos2 = (nodes[r[i+1]]['loc'][0]*scale, nodes[r[i+1]]['loc'][1]*scale)

            pygame.draw.line(screen, (100,255,0), pos1, pos2, 1)

    for n in r:
        if n > 0:
            pos = (nodes[n]['loc'][0]*scale, nodes[n]['loc'][1]*scale)
            pygame.draw.circle(screen, (100,255,0), pos, 3)

    pos = (nodes[r[len(r)-1]]['loc'][0]*scale, nodes[r[len(r)-1]]['loc'][1]*scale)
    pygame.draw.circle(screen,(255,100,100), pos, 3)
        
   
    pygame.display.flip()
    time.sleep(0.05)



pygame.quit()
    


    

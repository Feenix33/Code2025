"""
csp.py
Next attempt at BSP dungeon
Version c: simplify classes, don't worry about reuse; try bsp again

Next:
    make the paths be a new color if not on a room
    make the rooms smaller in the region
"""

import os
import math
import sys
import random

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from pygame.locals import *

sys.path.append('../cmeLib')
from cmePygameColors import *

#----- Dungeon --------------------------------------------------------------------------------

class Dungeon:
    crayons = [BLACK,ORANGE,YELLOW,RED,WHITE,BLUE,VIOLET,GREEN]
    def __init__(self, height, width, res, divs):
        self.height = height
        self.width = width
        self.res = res
        self.divs = divs
        self.grid = [[0 for i in range(width)] for j in range(height)]
        #for row in self.grid:
        #    print (row)
        self.rooms = []
        self.paths = []

    def reset(self):
        self.rooms = [Rect(0, 0, self.width, self.height)]
        self.grid = [[0 for i in range(self.width)] for j in range(self.height)]
        self.paths = []


    def draw(self, surf):
        rad = self.res/2-1
        y = self.res/2
        for row in self.grid:
            x = self.res/2
            for col in row:
                clr = Dungeon.crayons[col]
                pygame.draw.circle(surf, clr, (x, y), rad)
                x += self.res
            y += self.res

    def makePath(self, ra, rb): # path btwn room ra and room rb, return xy pts
        def xpart(x, xend, y, path):
            while x != xend:
                if x > xend: x -= 1
                elif x < xend: x += 1
                path.append((x,y))
        def ypart(y, yend, x, path):
            while y != yend:
                if y > yend: y -= 1
                elif y < yend: y += 1
                path.append((x,y))
        x = ra.left + random.randint(0, ra.width-1)
        y = ra.top + random.randint(0, ra.height-1)
        xend = rb.left + random.randint(0, rb.width-1)
        yend = rb.top + random.randint(0, rb.height-1)
        path = [(x,y)]
        if flip():
            xpart(x, xend, y, path)
            ypart(y, yend, x, path)
        else:
            ypart(y, yend, x, path)
            xpart(x, xend, y, path)
        return path

    def splitRoom(self, rect):
        # assume 0 is nothing
        if rect.width <= 3 or rect.height <= 3: return []
        if flip():
            #vert split
            w = int((rect.right-rect.left)/2)
            return [Rect(rect.left, rect.top, w, rect.height),
                    Rect(rect.left+w+1, rect.top, w-1, rect.height)]
        else:
            #horz split
            h = int((rect.bottom-rect.top)/2)
            return [Rect(rect.left, rect.top, rect.width, h),
                    Rect(rect.left, rect.top+h+1, rect.width, h-1)]

    def build(self):
        #reset
        self.reset()
        for _ in range(self.divs):
            newrooms = []
            for room in self.rooms:
                newrooms.extend(self.splitRoom(room))
            self.rooms = newrooms
        # make paths
        lvl = 2
        while lvl <= len(self.rooms):
            for n in range(0, len(self.rooms), lvl):
                self.paths.append(self.makePath(self.rooms[n], self.rooms[n+lvl-1]))
            lvl *= 2

        # put structures on grid
        for r in self.rooms:
            for y in range(r.top, r.bottom):
                for x in range(r.left, r.right):
                    self.grid[y][x] = 1
        for path in self.paths:
            for pt in path:
                if pt[1] >= self.height or pt[0] >= self.width:
                    print ("error ", pt)
                else:
                    self.grid[pt[1]][pt[0]] = 1

    def build01(self):
        #reset
        self.grid = [[1 for i in range(self.width)] for j in range(self.height)]
        # horz
        x = random.randint(0, int(len(self.grid[0])/2))
        y = random.randint(0, int(len(self.grid)/2))
        for yp in range(y,y+5):
            if yp < len(self.grid):
                for xp in range(x,x+8):
                    if xp < len(self.grid[0]):
                        self.grid[yp][xp] = 0

#----- Application --------------------------------------------------------------------------------
class MyApp:
    def __init__(self):
        # configuration
        cols = 80
        rows = 60
        res = 10
        divs = 2
        self.caption = "Hello recurse"
        self.width = res * cols
        self.height = res * rows 
        self.clrBackground = GREY
        #self.clrCrayons = [GREY,BLACK,RED,ORANGE,YELLOW,WHITE,BLUE,VIOLET,GREEN]

        # pseudo globals
        self.dungeon = Dungeon(rows, cols, res, divs)

        # operation
        self._running = True
        self.surf = None
        self.size = self.width, self.height 
        self.clock = pygame.time.Clock()
        self.font = None

    def on_init(self):
        pygame.display.set_caption(self.caption)
        pygame.init()
        self.surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)


    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False
        elif event.type == pygame.KEYUP:
            print ("key = ", event.key)
            if event.key == ord('n'):
                pass
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dungeon.build()
            #pos = pygame.mouse.get_pos()

    def on_loop(self):
        pass

    def draw(self):
        self.surf.fill(self.clrBackground)
        self.dungeon.draw(self.surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.draw()
            self.clock.tick(30)
        self.on_cleanup()


#----- My Utilities --------------------------------------------------------------------------------

def flip(p=0.5):
    return random.random() > p

#----- Main --------------------------------------------------------------------------------
if __name__ == "__main__":
    theApp = MyApp()
    theApp.on_execute()
    

"""
bisect.py
Build a maze from bisecting rectangles
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

#--------------------------------------------------------------------------------
class App:
    def __init__(self, config):
        self.CFG = config
        self._running = True
        self.surf = None
        self.size = self.width, self.height = self.CFG.width, self.CFG.height
        self.clock = pygame.time.Clock()
        self.font = None

    def on_init(self):
        pygame.display.set_caption(self.CFG.caption)
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
            pos = pygame.mouse.get_pos()

    def on_loop(self):
        pass

    def on_render(self):
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
            self.on_render()
            self.clock.tick(30)
        self.on_cleanup()


#--------------------------------------------------------------------------------

class MyApp(App):
    def __init__(self, cfg):
        super().__init__(cfg)

    def on_render(self):
        self.surf.fill(self.CFG.clrBackground)
        for r in range(self.CFG.rows):
            for c in range(self.CFG.cols):
                pygame.draw.rect(self.surf, 
                                 self.CFG.clrCrayons[ self.CFG.grid[r][c]],
                                 (c*self.CFG.res, r*self.CFG.res, self.CFG.res, self.CFG.res))
        pygame.display.flip()

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
            pos = pygame.mouse.get_pos()
            reset()

#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------

def output(n, rlist):
    for rect in rlist:
        print(f'{n:2}  ({rect.left:3}, {rect.top:3}) - ({rect.right:3}, {rect.bottom:3}) -- w={rect.w:3}, h={rect.h:3}')
    print ("-"*40)

def bisect(rect):
    if rect.w < 50 or rect.h < 50:
        return [rect]
    a = pygame.Rect.copy(rect)
    b = pygame.Rect.copy(a)
    first = a.width > a.height

    if first:
        w = a.width/4 + random.randint(1, int(a.width/2))
        a.width = w
        b.width -= w
        b.left = a.right
    else:
        h = a.height/4 + random.randint(1, int(a.height/2))
        a.height = h
        b.height -= h
        b.top = a.bottom
    return [a, b]

#--------------------------------------------------------------------------------
class WorldConfig:
    caption = "Hello recurse"
    res = 8
    cols = 81
    rows = 61
    width = res * cols #400
    height = res * rows #300
    clrBackground = MAGENTA
    clrCrayons = [GREY, YELLOW, BLUE, BROWN, GREEN]
    grid = None

    def __init__(self):
        WorldConfig.grid = [[0 for i in range(WorldConfig.cols)] 
                            for j in range (WorldConfig.rows)]

def divide(grid, top, bottom, left, right, level):
    if level > 3: return
    if (right-left) < 7 or (bottom-top) < 7: return
    print ("Divide ", top, bottom, left, right, level)
    if random.random() > 0.5: # horz
        split = random.randint(top+1, bottom-3) + 1
        if split%2==0: split+=1
        for n in range(left, right):
            grid[split][n] = 1
        #door at odd index
        door = random.randint(0, int((right-left)/2))*2 + left
        if door%2==0: door+=1
        grid[split][door] = 2
        divide (grid, top, split, left, right, level+1)
        divide (grid, split, bottom, left, right, level+1)
    else:
        split = random.randint(left+1, right-3) + 1
        if split%2==0: split+=1
        for n in range(top, bottom):
            grid[n][split] = 1
        #door at odd index
        door = random.randint(0, int((bottom-top)/2))*2 + top
        if door%2==0: door+=1
        grid[door][split] = 2
        divide (grid, top, bottom, left, split, level+1)
        divide (grid, top, bottom, split, right, level+1)

def reset():
    WorldConfig.grid = [[0 for i in range(WorldConfig.cols)] 
                        for j in range (WorldConfig.rows)]
    divide(WorldConfig.grid, 0, WorldConfig.rows, 0, WorldConfig.cols, 1)

#--------------------------------------------------------------------------------
if __name__ == "__main__":


    worldCfg = WorldConfig()
    #divide(WorldConfig.grid, 0, WorldConfig.rows, 0, WorldConfig.cols, 1)
    reset()
    theApp = MyApp(worldCfg)
    theApp.on_execute()
    

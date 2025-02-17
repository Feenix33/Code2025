"""
bsp.py
Attempt at BSP dungeon
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
        #pygame.display.flip()
        raise NotImplementedError

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
        """
        for r in range(self.CFG.rows):
            for c in range(self.CFG.cols):
                pygame.draw.rect(self.surf, 
                                 self.CFG.clrCrayons[ self.CFG.grid[r][c]],
                                 (c*self.CFG.res, r*self.CFG.res, self.CFG.res, self.CFG.res))
        """
        self.CFG.dungeon.draw(self.surf)
        pygame.display.flip()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False
        elif event.type == pygame.KEYUP:
            if event.key == ord('n'):
                worldCfg.reset()
                pass
            elif event.key == ord('d'):
                worldCfg.next_level()
            elif event.key == ord('l'):
                worldCfg.atLevel()
            elif event.key == ord('r'):
                worldCfg.buildRooms()
            elif event.key == ord('p'):
                worldCfg.buildPaths()
            else:
                print ("key = ", event.key)
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            worldCfg.buildDungeon()

#--------------------------------------------------------------------------------
class DungeonSpace:
    def __init__(self, rect, lvl):
        self.space = rect.copy()
        self.c1 = None # child
        self.c2 = None # child
        self.lvl = lvl
        self.room = None
        self.path = []

    def buildPaths(self):
        if self.c1.room:
            x1 = int(self.c1.room.left + self.c1.room.width/2)
            y1 = int(self.c1.room.right + self.c1.room.height/2)
            x2 = int(self.c2.room.left + self.c2.room.width/2)
            y2 = int(self.c2.room.right + self.c2.room.height/2)
            xbgn = min(x1, x2)
            xend = max(x1, x2)
            ybgn = min(y1, y2)
            yend = max(y1, y2)
            print ("Paths", xbgn, xend, ybgn, yend)
            while (xbgn < xend and ybgn < yend):
                self.c1.path.append((xbgn, ybgn))
                if xbgn < xend: xbgn += 1
                if ybgn < yend: ybgn += 1
        else:
            self.c1.buildPaths()
            self.c2.buildPaths()

    
    def buildRooms(self):
        if self.c1 == None: #if not none this has been divided
            # good to build a room
            def ranPortion(v,n): # helper function
                return random.randint(int(v/n), (n-1)*int(v/n))
            self.room = self.space.copy()
            olddim = self.room.height
            self.room.height = ranPortion(self.room.height,4)
            margin = olddim - self.room.height
            self.room.top = self.room.top + ranPortion(margin,8)

            olddim = self.room.width
            self.room.width = ranPortion(self.room.width, 4)
            margin = olddim - self.room.width
            self.room.left = self.room.left + ranPortion(margin,8) 
        else:
            self.c1.buildRooms()
            self.c2.buildRooms()

    def getLevel(self):
        if self.c1 == None:
            return self.lvl
        else:
            return self.c1.getLevel()

    def divide(self):
        if self.room == None:
            if self.c1 == None: #if not none this has been divided
                if self.space.width > self.space.height:
                    self.divideVert()
                else:
                    self.divideHorz()
                """
                ratio = self.space.width/self.space.height
                if ratio < 0.25:
                    self.divideHorz()
                elif ratio > 4.00:
                    self.divideVert()
                elif random.random() < 0.5:
                    self.divideVert()
                else:
                    self.divideHorz()
                """
            else:
                self.c1.divide()
                self.c2.divide()

    def divideVert(self):
        split = random.randint(int(self.space.width/4), int(3*self.space.width/4))
        self.c1 = DungeonSpace(self.space, self.lvl+1)
        self.c1.space.width = split

        self.c2 = DungeonSpace(self.space, self.lvl+1)
        self.c2.space.width = self.c2.space.width - split
        self.c2.space.left += split

    def divideHorz(self):
        split = random.randint(int(self.space.height/4), int(3*self.space.height/4))
        self.c1 = DungeonSpace(self.space, self.lvl+1)
        self.c1.space.height = split

        self.c2 = DungeonSpace(self.space, self.lvl+1)
        self.c2.space.height = self.c2.space.height - split
        self.c2.space.top += split

    def draw(self, surf):
        crayons = [RED, WHITE, BLUE, GREEN, YELLOW, GREY, PINK, ORANGE]
        clr = crayons[self.lvl % len(crayons)]
        
        #pygame.draw.rect(surf, clr, self.space)
        pygame.draw.rect(surf, BLACK, self.space, width=1)
        if self.room:
            pygame.draw.rect(surf, BLACK, self.room, width=0)
        if len(self.path) > 0:
            for pt in self.path:
                pygame.draw.circle(surf, YELLOW, pt, 2)

        if self.c1: self.c1.draw(surf)
        if self.c2: self.c2.draw(surf)

class Level:
    def __init__(self, left, top, right, bottom, lvl):
        self.space = pygame.Rect(left, top, right, bottom)
        self.c1 = None # child
        self.c2 = None # child
        self.lvl = lvl

    def generate(self):
        if self.c1 == None: #implies subdivide this parent
            # start w/horz split
            splitAt = int((self.space.bottom - self.space.top)/2)
            self.c1 = self.space.copy() # copy the original then cut
            self.c1.height = int(self.c1.height/2)
            self.c2 = self.space.copy() # copy the original then cut
            self.c2.height = int(self.c2.height/2)
            self.c2.top = self.space.top+self.c2.height


    def draw(self, surf):
        if self.c1 == None and self.c2 == None:
            pygame.draw.rect(surf, GREY, self.space)
        else:
            if self.c1 != None:
                pygame.draw.rect(surf, RED, self.c1)
            if self.c2 != None:
                pygame.draw.rect(surf, BLUE, self.c2)


class WorldConfig:
    caption = "Hello recurse"
    res = 5
    cols = 80
    rows = 50
    width = res * cols
    height = res * rows 
    clrBackground = GREY
    #clrCrayons = [GREY, YELLOW, BLUE, RED, BROWN, GREEN]
    clrCrayons = [GREY,BLACK,RED,ORANGE,YELLOW,WHITE,BLUE,VIOLET,GREEN]
    grid = None
    dungeon = DungeonSpace(pygame.Rect(0, 0, width, height), 1)

    def __init__(self):
        self.reset()

    def buildDungeon(self):
        self.reset()
        while self.dungeon.getLevel() < 4:
            self.dungeon.divide()
        self.dungeon.buildRooms()

    def buildRooms(self):
        self.dungeon.buildRooms()

    def buildPaths(self):
        self.dungeon.buildPaths()

    def next_level(self):
        self.dungeon.divide()

    def atLevel(self):
        print (self.dungeon.getLevel())

    def reset(self):
        #WorldConfig.grid = [[0 for i in range(WorldConfig.cols)] 
        #                    for j in range (WorldConfig.rows)]
        #generate_level(WorldConfig.grid, 0, 0, WorldConfig.rows, WorldConfig.cols, 1, 0)
        WorldConfig.dungeon = DungeonSpace(pygame.Rect(0, 0, WorldConfig.width, WorldConfig.height), 1)

#--------------------------------------------------------------------------------

def flip(p=0.5):
    return random.random() > p

def generate_level(grid, left, top, right, bottom, val, level):
    if level >= 4: 
        for r in range(top+2, bottom-2):
            for c in range(left+2, right-2):
                grid[c][r] = val+1
        return

    if flip(): # horiz
        #mid = int((bottom-top)/2) + top
        if bottom-top < 20: return
        quad = int((bottom-top)/4) 
        mid = top + random.randint(quad, quad*3)
        for n in range(left, right):
            grid[n][mid] = val
        generate_level(grid, left, top, right, mid, val, level+1)
        generate_level(grid, left, mid, right, bottom, val, level+1)

    else:
        if right-left < 20: return
        #mid = int((right-left)/2) + left
        quad = int((right-left)/4) 
        mid = left + random.randint(quad, quad*3)
        for n in range(top, bottom):
            grid[mid][n] = val
        generate_level(grid, left, top, mid, bottom, val, level+1)
        generate_level(grid, mid, top, right, bottom, val, level+1)


#--------------------------------------------------------------------------------
if __name__ == "__main__":
    worldCfg = WorldConfig()
    theApp = MyApp(worldCfg)
    theApp.on_execute()
    

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
        self.make_rooms()

    def make_rooms(self):
        self.rooms = []
        self.rooms.append(pygame.Rect(0, 0, self.CFG.width, self.CFG.height))

        for j in range(self.CFG.splits):
            newRooms = []
            for room in self.rooms:
                newRooms = newRooms + bisect(room)
            self.rooms = newRooms.copy()

    def on_render(self):
        self.surf.fill(self.CFG.clrBackground)
        for room in self.rooms:
            pygame.draw.rect(self.surf, YELLOW, room, width=2) 
        pygame.display.flip()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.CFG.splits += 1
                self.make_rooms()
            elif event.key == pygame.K_DOWN:
                self.CFG.splits -= 1
                self.make_rooms()
            elif event.key == ord('n'):
                pass
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.make_rooms()

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
if __name__ == "__main__":
    class WorldConfig:
        caption = "Hello bisect"
        width = 400
        height = 300
        clrBackground = GREEN
        splits = 3

    worldCfg = WorldConfig()
    theApp = MyApp(worldCfg)
    theApp.on_execute()
    
    """
    rooms = []
    rooms.append(pygame.Rect(0, 0, 200, 100))

    for j in range(3):
        newRooms = []
        for room in rooms:
            newRooms = newRooms + bisect(room)
        rooms = newRooms.copy()

        #output(j+1, rooms)
    """

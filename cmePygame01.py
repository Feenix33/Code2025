"""
decor.py
Pygame demo of alternative to inheritance
"""

import os
import random
import math
import sys

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

class AppDecor(App):
    def __init__(self, cfg):
        super().__init__(cfg)

    def on_render(self):
        self.surf.fill(self.CFG.clrBackground)
        pygame.display.flip()

#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
if __name__ == "__main__":
    class Config:
        caption = "Hello Decor"
        width = 400
        height = 300
        clrBackground = GREEN

    globCfg = Config()
    theApp = AppDecor(globCfg)
    theApp.on_execute()
            

"""
viewport.py
Pygame demo simulating multiple panels
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
class Viewport:
    def __init__(self, rect, clrBack):
        self.rect = rect
        self.clrBackground = clrBack
        self.surf = pygame.Surface((self.rect.width, self.rect.height))
        self.surf.fill(self.clrBackground)

    def render(self, display):
        display.blit(self.surf, self.rect)

    def update(self):
        pass
    
class MainView(Viewport):
    def __init__(self):
        super().__init__(pygame.Rect(0, 0, 400, 400), BLUE)
        self.tx = 100

    def render(self, display):
        self.surf.fill(self.clrBackground)

        pygame.draw.rect(self.surf, WHITE, pygame.Rect(100, 100, 80, 50))
        tstr = "abc = " + str(CFG.width)
        text = CFG.font.render(tstr,  True, GREEN, BLUE)
        self.surf.blit(text, (self.tx, 200))

        super().render(display)

    def update(self):
        if self.tx < 300:
            self.tx += 1

class StatusView(Viewport):
    def __init__(self):
        super().__init__(pygame.Rect(400, 200, 200, 200), BLACK)
        self.tx = 10

    def render(self, display):
        self.surf.fill(self.clrBackground)
        tstr = "abc = " + str(CFG.width)
        text = CFG.font.render(tstr,  True, YELLOW)
        self.surf.blit(text, (self.tx, 20))
        super().render(display)

#--------------------------------------------------------------------------------
class AppConfig:
    width = 600
    height = 400
    font = None

    def __init__(self):
        pygame.font.init()
        AppConfig.font = pygame.font.Font(pygame.font.get_default_font(), 12)

#--------------------------------------------------------------------------------
class App:
    def __init__(self):
        self._running = True
        self.surf = None
        self.size = self.width, self.height = CFG.width, CFG.height
        self.clock = pygame.time.Clock()

    def on_init(self):
        pygame.display.set_caption("Viewport")
        pygame.init()
        self.surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True


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
class ViewportApp(App):
    def __init__(self):
        super().__init__()
        pygame.font.init()
        self.views= [
                MainView(),
                Viewport(pygame.Rect(400, 0, 200, 200), YELLOW),
                StatusView(),
                ]
        #Viewport(pygame.Rect(400, 200, 200, 200), BLACK),

    def on_render(self):
        for view in self.views:
            view.render(self.surf)
        pygame.display.flip()
        
    def on_loop(self):
        for view in self.views:
            view.update()

#--------------------------------------------------------------------------------
if __name__ == "__main__":
    CFG = AppConfig()
    theApp = ViewportApp()
    theApp.on_execute()
            

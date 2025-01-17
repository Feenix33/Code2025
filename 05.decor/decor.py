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

class Critter(pygame.sprite.Sprite):
    def __init__(self, breed, world):
        self.breed = breed
        self.world = world
        self.image = pygame.Surface((breed.width, breed.height))
        self.image.fill(breed.clr)
        self.rect = self.image.get_rect()
        self.rect.x = 100 + random.randint(0, 200)
        self.rect.y = 50 + random.randint(0, 200)
        self.vel = pygame.math.Vector2(2, -3)
        heading = random.randint(0, 360)
        self.vel = pygame.math.Vector2.from_polar((1, heading)) * self.breed.speed
    def render(self, display):
        display.blit(self.image, self.rect)
        if hasattr(self.breed, 'update'):
            self.breed.update(self.breed, self)

class BreedAlpha:
    clr = BLUE
    width = 25
    height = 15
    speed = 5

    def __init__(self):
        pass

    def update(self, critter):
        critter.rect.x += critter.vel.x
        critter.rect.y += critter.vel.y
        if critter.rect.x < 0:
            critter.rect.x = 0
            critter.vel.x *= -1
        elif critter.rect.x > critter.world.width-critter.rect.width:
            critter.rect.x = critter.world.width-critter.rect.width
            critter.vel.x *= -1
        if critter.rect.y < 0:
            critter.rect.y = 0
            critter.vel.y = -(critter.vel.y)
        elif critter.rect.y > critter.world.height-critter.rect.height:
            critter.rect.y = critter.world.height-critter.rect.height
            critter.vel.y = -(critter.vel.y)

class BreedBravo:
    clr = YELLOW
    width = 15
    height = 15
    speed = 8

    def __init__(self):
        pass

    def update(self, critter):
        critter.rect.x += critter.vel.x
        critter.rect.y += critter.vel.y
        bounce = False
        if critter.rect.x < 0:
            critter.rect.x = 0
            critter.vel.x *= -1
        elif critter.rect.x > critter.world.width-critter.rect.width:
            critter.rect.x = critter.world.width-critter.rect.width
            critter.vel.x *= -1
        if critter.rect.y < 0:
            critter.rect.y = 0
            critter.vel.y = -(critter.vel.y)
        elif critter.rect.y > critter.world.height-critter.rect.height:
            critter.rect.y = critter.world.height-critter.rect.height
            critter.vel.y = -(critter.vel.y)
        

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
        self.critters = []
        self.critters.append(Critter(BreedAlpha, cfg))
        self.critters.append(Critter(BreedBravo, cfg))

    def on_render(self):
        self.surf.fill(self.CFG.clrBackground)
        for critter in self.critters:
            critter.render(self.surf)
        pygame.display.flip()

#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
if __name__ == "__main__":
    class WorldConfig:
        caption = "Hello Decor"
        width = 400
        height = 300
        clrBackground = GREEN

    worldCfg = WorldConfig()
    theApp = AppDecor(worldCfg)
    theApp.on_execute()
            

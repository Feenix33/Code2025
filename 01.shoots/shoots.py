"""
shoots.py
Pygame demo simulating a shoot-em-up game
"""
# TODO
# convert xywh to the rect
# collsion with masks
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from pygame.locals import *
import random
import math

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = ( 0,255, 0)
BLUE = ( 0, 0,255)
YELLOW = (255,255,  0)
CYAN = (  0,255,255)
MAGENTA = (255,  0,155)
GREY = (127,127,127)
PINK = (255,192,203)


class Thing(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._vx = vx
        self._vy = vy
        self._surf = pygame.Surface([w,h])
        self._surf.fill(MAGENTA)
        self._surf.set_colorkey(MAGENTA)
        #self.rect = pygame.Rect(x, y, w, h)
        self.rect = self._surf.get_rect()
        self._alive = True

    def draw(self, display):
        if self._alive and self._surf:
            display.blit(self._surf, (self._x, self._y))

    def update(self):
        self._x += self._vx
        self._y += self._vy
        self.rect = pygame.Rect(self._x, self._y, self._w, self._h)

    def moveTo(self, x, y):
        self._x = x
        self._y = y

class Ship(Thing):
    def __init__(self, x, y, w, h, vx, vy):
        super().__init__(x, y, w, h, vx, vy)
        #pygame.draw.polygon(self._surf, (0,0,255), [(0, 0), (0,h), (w,h)], width=0)
        pygame.draw.polygon(self._surf, BLUE, [(0,0), (0,h),(w/2,h/2)], width=0)
        pygame.draw.line(self._surf, BLUE, (0,h/2),(w,h/2), width=3)

    def update(self):
        r = random.random() 
        if r > 0.8  and r <= 0.85:
            self._vy = -1
        elif r > 0.85 and r <= 0.90:
            self._vy =  1
        elif r > 0.90:
            self._vy = 0
        self._x += self._vx
        self._y += self._vy
        if self._y < 100:
            self._y = 100
        if self._y > 300:
            self._y = 300
        self.rect = pygame.Rect(self._x, self._y, self._w, self._h)

    def fire(self):
        return Torpedo(self._x, self._y, 10, 4, 10, self._vy)


class Torpedo(Thing):
    def __init__(self, x, y, w, h, vx, vy):
        super().__init__(x, y, w, h, 0, 0)
        self._surf.fill(RED)
        self._vx = vx
        self._vy = vy
    def update(self):
        super().update()
        if self._alive and self._x > 640 or self._y < 0 or self._y > 400:
            self._alive = False
        self.rect = pygame.Rect(self._x, self._y, self._w, self._h)

class Bogie(Thing):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, 0, 0)
        self.respawn()
        self._x = x
        self._y = y
        pygame.draw.rect(self._surf, GREEN, pygame.Rect(w/2, 0, w/2, h))
        pygame.draw.circle(self._surf, GREEN,(w/2,h/2),h/2) 
    def respawn(self):
        self._vx = -random.randint(1,6)
        self._vy = 0
        self._y = random.randint(50, 350)
        self._yoff = self._y
        self._x = 640+50
        self._alive = True
        self._amp = random.randint(10, 80)
    def update(self):
        if self._alive:
            self._x += self._vx
            self._y = self._amp * math.sin(self._x * 3.1415 / 90) + self._yoff
            if self._x < -100: self._alive = False
        else:
            self.respawn()
        self.rect = pygame.Rect(self._x, self._y, self._w, self._h)

class App:
    def __init__(self):
        self._running = True
        self._surf = None
        self.size = self.width, self.height = 640, 400
        self.things = None
        self.clock = pygame.time.Clock()

    def on_init(self):
        pygame.display.set_caption("Shoots")
        pygame.init()
        self._surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        self.grpShips = pygame.sprite.Group()
        self.grpTorps = pygame.sprite.Group() 
        self.grpBogies = pygame.sprite.Group()
        self.grpThings = pygame.sprite.Group()

        self.ship = Ship(100, 50, 30, 15, 0, 0)
        self.add_sprite2groups(self.ship, self.grpShips)

        for j in range(5):
            self.add_sprite2groups(Bogie(500+j*10, 50+j*50, 20, 10), self.grpBogies)


    def add_sprite2groups(self, sprite, group=None):
        self.grpThings.add(sprite)
        if group != None:
            group.add(sprite)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False
        if event.type == pygame.KEYUP:
            print ("key = ", event.key)
            if event.key == ord('n'):
                print ("Bogies    :", len(self.grpBogies))
                print ("Torps     :", len(self.grpTorps ))
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.add_sprite2groups(self.ship.fire(), self.grpTorps)
            self.add_sprite2groups(self.mouseFire(pos[0], pos[1]), self.grpTorps)

    def mouseFire(self, x, y):
        return Torpedo(x, y, 20, 8, 10, 0)
    
    def on_loop(self):
        for thing in self.grpThings:
            thing.update()

        # collision detection
        for bogie in self.grpBogies.sprites():
            collides = pygame.sprite.spritecollide(bogie, self.grpTorps, True)
            if len(collides) > 0:
                bogie.kill()


        nbgn = len(self.grpTorps)
        for torp in self.grpTorps:
            if not torp._alive:
                torp.kill()
        nend = len(self.grpTorps)
        #if nbgn != nend: print ("Torps = ", len(self.grpTorps))


    def on_render(self):
        self._surf.fill((128,128,128))
        #pygame.draw.rect(self._surf, (255,0,0),pygame.Rect(30,30, 60,60))
        #for thing in self.things:
        for thing in self.grpThings:
            thing.draw(self._surf)
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


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
            

"""
shoots.py
Pygame demo simulating a shoot-em-up game
"""
# TODO
# collsion with masks
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
from pygame.locals import *
import random
import math
from cmePygameColors import *

FIRE_EVENT = pygame.USEREVENT + 1
BOGIE_FIRE_EVENT = pygame.USEREVENT + 2

class Thing(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, vx, vy):
        pygame.sprite.Sprite.__init__(self)
        self.vx = vx
        self.vy = vy
        self.surf = pygame.Surface([w,h])
        self.surf.fill(MAGENTA)
        self.surf.set_colorkey(MAGENTA)
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.alive = True

    def draw(self, display):
        if self.alive and self.surf:
            #display.blit(self.surf, (self.rect.x, self.rect.y))
            display.blit(self.surf, self.rect)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

class Ship(Thing):
    def __init__(self, x, y, w, h, vx, vy):
        super().__init__(x, y, w, h, vx, vy)
        #pygame.draw.polygon(self.surf, (0,0,255), [(0, 0), (0,h), (w,h)], width=0)
        pygame.draw.polygon(self.surf, BLUE, [(0,0), (0,h),(w/2,h/2)], width=0)
        pygame.draw.line(self.surf, BLUE, (0,h/2),(w,h/2), width=3)
        self.shotTimer = 0
        self.shieldTimer = 30

    def update(self):
        r = random.random() 
        if r > 0.8  and r <= 0.85:
            self.vy = -1
        elif r > 0.85 and r <= 0.90:
            self.vy =  1
        elif r > 0.90:
            self.vy = 0
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.y < 100:
            self.rect.y = 100
        if self.rect.y > 300:
            self.rect.y = 300
        if self.shotTimer <= 0:
            self.triggerFire()
            self.shotTimer = 30
        else:
            self.shotTimer -= 1
        self.shieldTimer -= 1

    def fire(self):
        return [Torpedo(self.rect.x+self.rect.w/2, self.rect.y+(self.rect.h/2),  5, 5, 10, -3, MEDIUMBLUE),
                Torpedo(self.rect.x+self.rect.w/2, self.rect.y                ,  5, 5, 10, 0, MEDIUMBLUE),
                Torpedo(self.rect.x+self.rect.w/2, self.rect.y+(self.rect.h  ),  5, 5, 10, 3, MEDIUMBLUE)]

    def triggerFire(self):
        event_data = {'message': 'Custom event triggered'}
        my_event = pygame.event.Event(FIRE_EVENT, event_data)
        pygame.event.post(my_event)

    def draw(self, surf):
        super().draw(surf)
        if self.shieldTimer >= 0:
            pygame.draw.circle(surf, BLUE,(self.rect.x+self.rect.w/2, self.rect.y+self.rect.h/2),(self.rect.w +self.rect.h)/2, width=1)

    def shieldOn(self, t=-1):
        self.shieldTimer = 30

class Torpedo(Thing):
    def __init__(self, x, y, w, h, vx, vy, clr=None):
        super().__init__(x, y, w, h, 0, 0)
        if clr == None: clr = RED
        self.surf.fill(clr)
        self.vx = vx
        self.vy = vy
    def update(self):
        super().update()
        if self.alive and self.rect.x > 640 or self.rect.x < 0 or self.rect.y < 0 or self.rect.y > 400:
            self.alive = False

class Bogie(Thing):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, 0, 0)
        self.respawn()
        self.rect.x = x
        self.rect.y = y
        pygame.draw.circle(self.surf, LIME,(w/2,h/2),h/2) 
        pygame.draw.rect(self.surf, GREEN, pygame.Rect(w/2, 0, w/2, h))
        self.shotTimer = -1

    def respawn(self):
        self.vx = -random.randint(1,6)
        self.vy = 0
        self.rect.y = random.randint(50, 350)
        self.yoff = self.rect.y
        self.rect.x = 640+50
        self.alive = True
        self._amp = random.randint(10, 80)

    def update(self):
        if self.alive:
            self.rect.x += self.vx
            self.rect.y = self._amp * math.sin(self.rect.x * 3.1415 / 90) + self.yoff
            if self.rect.x < -100: self.alive = False
        else:
            self.respawn()
        #self.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)
        self.shotTimer -= 1
        if self.shotTimer == 0:
            self.triggerFire()
        elif self.shotTimer < 0:
            self.shotTimer = random.randint(10,60)

    def triggerFire(self):
        x = 639 if self.rect.x > 640 else self.rect.x
        event_data = {'message': 'Bogie fire triggered', 
                      'bogie': self,
                      'x':x, 'y':self.rect.y}
        my_event = pygame.event.Event(BOGIE_FIRE_EVENT, event_data)
        pygame.event.post(my_event)


class App:
    def __init__(self):
        self._running = True
        self.surf = None
        self.size = self.width, self.height = 640, 400
        self.things = None
        self.clock = pygame.time.Clock()

    def on_init(self):
        pygame.display.set_caption("Shoots")
        pygame.init()
        self.surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

        self.grpShips = pygame.sprite.Group()
        self.grpTorps = pygame.sprite.Group() 
        self.grpFlak = pygame.sprite.Group() 
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
        # if isinstance(group, list): group is a list of groups

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._running = False
        elif event.type == pygame.KEYUP:
            print ("key = ", event.key)
            if event.key == ord('n'):
                print ("Bogies    :", len(self.grpBogies))
                print ("Torps     :", len(self.grpTorps ))
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            #self.ship.shieldOn()
        elif event.type == FIRE_EVENT:
            self.add_sprite2groups(self.ship.fire(), self.grpTorps)
        elif event.type == BOGIE_FIRE_EVENT:
            self.add_sprite2groups(
                Torpedo(event.x, event.y, 3, 3, -10, 0, YELLOW), self.grpFlak)


    def mouseFire(self, x, y):
        return Torpedo(x, y,  5, 5, 10, 0)
    
    def on_loop(self):
        for thing in self.grpThings:
            thing.update()

        # collision detection
        for bogie in self.grpBogies.sprites():
            collides = pygame.sprite.spritecollide(bogie, self.grpTorps, True)
            if len(collides) > 0:
                bogie.kill()

        for torp in self.grpTorps:
            if not torp.alive:
                torp.kill()

        if len(self.grpBogies) < 5:
            self.add_sprite2groups(Bogie(680, random.randint(50,350), 20, 10), self.grpBogies)

        # enemy torpodo detection
        collides = pygame.sprite.spritecollide(self.ship, self.grpFlak, True)
        if len(collides) > 0:
            self.ship.shieldOn()
        # enemy collision detection
        collides = pygame.sprite.spritecollide(self.ship, self.grpBogies, True)
        if len(collides) > 0:
            self.ship.shieldOn()


    def on_render(self):
        self.surf.fill(DIMGREY)
        for thing in self.grpThings:
            thing.draw(self.surf)
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
            

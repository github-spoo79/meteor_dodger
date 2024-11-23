import pygame
import random
import math
from enviroment import Enviroment as env
from util import Util

class Effect():
    def __init__(self, main):
        self.main = main
        self.effect0 = main.resources.effect0
        self.effect1 = main.resources.effect1
        self.effect2 = main.resources.effect2
        self.effect3 = main.resources.effect3
        self.effect4 = main.resources.effect4
        self.explosion0 = main.resources.explosion0
        self.explosion1 = main.resources.explosion1
        self.explosion2 = main.resources.explosion2
        self.explosion3 = main.resources.explosion3

    def radial_explode(self, id, x, y, size, cnt):
        for _ in range(cnt):
            size = random.randint(int(size / 2), size)
            dir = random.randint(0, 359)            
            self.main.effect_sprites.add(Particle(x, y, size, dir, getattr(self, "effect" + str(id))))
            
    def circle_explode(self, x, y, size, cnt):
        for _ in range(cnt):      
            max_size =  random.randint(int(size/2), size)
            dir = random.randint(0, 359)
            theta = math.radians(dir)
            r = (size/2) * math.sqrt(random.uniform(0, 1))
            tx = x + r * math.cos(theta)
            ty = y + r * math.sin(theta)
            self.main.effect_sprites.add(Explosion(tx, ty, max_size, getattr(self, "explosion0")))
            
        for _ in range(int(cnt/2)):      
            #max_size =  random.randint(int(size/2), size)
            max_size = size
            dir = random.randint(0, 359)
            theta = math.radians(dir)
            r = (size/4) * math.sqrt(random.uniform(0, 1))
            tx = x + r * math.cos(theta)
            ty = y + r * math.sin(theta)
            color = random.choice(['1', '2', '3'])
            self.main.effect_sprites.add(Explosion(tx, ty, max_size, getattr(self, "explosion" + str(color))))
        
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, size, dir, sprites):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = sprites
        self.size = size
        self.image = sprites[size]
        self.rect = self.image.get_rect()
        self.pos = (x, y)
        self.rect.center = (x, y)
        self.speed = random.uniform(0.5, 2)
        self.target = pygame.Vector2(env.ANGLE_TO_VECTORS[dir])
        self.vel = self.target * self.speed
        self.shrink_delay_frame = 10
        self.frame = 0
        self.inc = -1
        self.gravity_vel = 0.8
        
    def update(self):
        self.frame += 1
        if self.frame % env.FPS == 0:
            self.frame = 0
        
        if self.frame % self.shrink_delay_frame == 0:
            self.size += self.inc

        if self.size < 0:
            self.kill()

        self.vel = self.target * self.speed
        self.vel.y += self.gravity_vel
        self.image = self.sprites[self.size]
        self.rect = self.image.get_rect()
        self.pos += self.vel
        self.rect.center = self.pos
        

class Explosion(pygame.sprite.Sprite):     
    def __init__(self, x, y, max_size, sprites):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = sprites
        self.idx = 0
        self.image = sprites[self.idx]
        self.rect = self.image.get_rect()
        self.pos = (x, y)
        self.rect.center = self.pos
        self.frame = 0
        self.max_size = max_size
        self.opacity = 255
        
    def update(self):
        if self.idx > len(self.sprites) - 1 or self.idx >= self.max_size:
            self.opacity -= 10
            self.image = Util.set_opacity(self.image, self.opacity)
            if self.opacity <= 0:
                self.kill()
        else:
            self.idx += 2
            self.image = self.sprites[self.idx]
        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
                    

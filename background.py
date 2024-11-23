import pygame
import random
from enviroment import Enviroment as env

class Background:
    def __init__(self):
        self.stars = [Star() for _ in range(env.TOTAL_STARS_COUNT)]

    def draw(self, screen):
        for star in self.stars:
            star.move()
            star.draw(screen)

class Star:
    def __init__(self):
        self.x = random.randint(0, env.WIDTH)
        self.y = random.randint(-10, env.HEIGHT)
        self.speed = random.randint(env.MIN_STARS_SPEED, env.MAX_STARS_SPEED)
        self.size = 1
    
    def move(self):
        self.y += self.speed
        if self.y > env.HEIGHT:
            self.y = random.randint(-10, -5)
            self.x = random.randint(0, env.WIDTH)
            self.speed = self.init_stars()

    def init_stars(self):
        if random.randint(1, env.UTRLA_SPEED_CHANCE) == 1:
            speed = env.UTRLA_STARS_SPEED
        else:
            speed = random.randint(env.MIN_STARS_SPEED, env.MAX_STARS_SPEED)                    
        return speed


    def draw(self, screen):
        pygame.draw.circle(screen, env.WHITE, (self.x, self.y), self.size)

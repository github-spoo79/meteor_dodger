import pygame
import random
from enviroment import Enviroment as env

class Item(pygame.sprite.Sprite):
    def __init__(self, s_pos, d_pos, main):
        super().__init__()
        self.speed = 1
        self.target = (pygame.Vector2(d_pos) - pygame.Vector2(s_pos))
        self.target.normalize_ip()
        self.velocity = self.target * self.speed
        self.mass = 0  
        self.damage = 0
        self.id = "item"      
        self.effect_id = "0"
        self.main = main
        
    def update(self):
        self.move()
        self.dispose()
        
    def move(self):
        self.velocity = self.target * self.speed
        self.pos += self.velocity
        self.rect.center = (self.pos)                   
        
    def dispose(self):
        if self.rect.x + self.rect.width + env.MARGIN < 0:
            self.kill()
        elif self.rect.x + self.rect.width - env.MARGIN >= env.WIDTH:
            self.kill()
        elif self.rect.y + self.rect.height + env.MARGIN < 0:
            self.kill()
        elif self.rect.y + self.rect.height - env.MARGIN >= env.HEIGHT:
            self.kill()        

class ItemShield(Item):
    def __init__(self, s_pos, d_pos, main):
        super().__init__(s_pos, d_pos, main)
        self.image = main.resources.item_shield
        self.rect = self.image.get_rect()
        self.rect.center = s_pos
        self.pos = s_pos
        
    def handle_collision(self, t_velocity, t_mass, damage):
        self.main.player.create_shield()
        self.main.sound_effect.make_sound("player_upgrade")
        self.kill()

class ItemPower(Item):
    def __init__(self, s_pos, d_pos, main):
        super().__init__(s_pos, d_pos, main)
        self.image = main.resources.item_power
        self.rect = self.image.get_rect()
        self.rect.center = s_pos
        self.pos = s_pos
        
    def handle_collision(self, t_velocity, t_mass, damage):
        self.main.player.power_up()
        self.main.sound_effect.make_sound("player_upgrade")
        self.kill()
        
class ItemJewerly(Item):
    def __init__(self, s_pos, d_pos, main):
        super().__init__(s_pos, d_pos, main)
        self.image = main.resources.item_jewerly
        self.rect = self.image.get_rect()
        self.rect.center = s_pos
        self.pos = s_pos
        
    def handle_collision(self, t_velocity, t_mass, damage):
        self.main.player.jewerly_up()
        self.main.sound_effect.make_sound("player_jewerly")
        self.kill()
    
class ItemEnergy(Item):
    def __init__(self, s_pos, d_pos, main):
        super().__init__(s_pos, d_pos, main)
        self.image = main.resources.item_energy
        self.rect = self.image.get_rect()
        self.rect.center = s_pos
        self.pos = s_pos
        
    def handle_collision(self, t_velocity, t_mass, damage):
        self.main.player.health_up()
        self.main.sound_effect.make_sound("player_upgrade")
        self.kill()

class ItemBomb(Item):
    def __init__(self, s_pos, d_pos, main):
        super().__init__(s_pos, d_pos, main)
        self.image = main.resources.item_bomb
        self.rect = self.image.get_rect()
        self.rect.center = s_pos
        self.pos = s_pos
        
    def handle_collision(self, t_velocity, t_mass, damage):
        self.main.player.bomb_up()
        self.kill()
        

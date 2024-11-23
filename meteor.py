import pygame
import random
from enviroment import Enviroment as env
from util import Util
from item import ItemShield, ItemJewerly, ItemPower, ItemEnergy, ItemBomb

class Meteor(pygame.sprite.Sprite):
    def __init__(self, s_pos, d_pos, resource, mass, effect_id):
        super().__init__()
        self.sprites = resource
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.center = (s_pos)
        self.pos = s_pos
        self.speed = random.randint(1, 5)
        self.target = (pygame.Vector2(d_pos) - pygame.Vector2(s_pos))
        self.target.normalize_ip()
        self.velocity = self.target * self.speed
        self.rotate_speed = random.randint(1, 3) * random.choice([-1, 1])
        self.image_idx = 0
        self.mass = mass
        self.damage = 1
        self.id = "enemy"
        self.group_id = "enemy"
        # 체력 속성 추가, 체력이 모두 떨어지면 destroy 처리
        self.health = (mass + 5) / 5
        self.effect_id = effect_id

    def update(self, main):
        if self.health >= 0:
            self.rotate()
            self.move()
            self.dispose()
        else:
            self.destroy(main)

    def destroy(self, main):
        cnt = random.randint(6, 8)
        main.effect.circle_explode(self.rect.centerx, self.rect.centery, self.mass, cnt)
        main.effect.radial_explode(self.effect_id, self.rect.centerx, self.rect.centery, int(self.mass / 3), 100)
        
        if Util.is_probability(env.ITEM_CHANCE):
            s_pos = (self.rect.centerx, self.rect.centery)
            d_pos = (main.player.pos.x, main.player.pos.y)
            if Util.is_probability(env.ITEM_CHANCE):                
                item_type = random.choice(['1', '2', '3', '4'])                
                if item_type == '1':
                    item = ItemShield(s_pos, d_pos, main)
                elif item_type == '2':
                    item = ItemPower(s_pos, d_pos, main)
                elif item_type == '3':
                    item = ItemEnergy(s_pos, d_pos, main)        
                else:
                    item = ItemBomb(s_pos, d_pos, main)
            else:
                item = ItemJewerly(s_pos, d_pos, main)
                
            main.item_sprites.add(item)
        main.sound_effect.make_sound("enemy_explosion")
        self.kill()

    def rotate(self):        
        self.image_idx += self.rotate_speed        
        if self.image_idx >= 360:
            self.image_idx = 0
        elif self.image_idx < 0:
            self.image_idx = 359
        
    def move(self):
        self.velocity = self.target * self.speed
        self.pos += self.velocity
        self.image = self.sprites[self.image_idx]
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos)

    def handle_collision(self, t_velocity, t_mass, damage):    
        self.health -= damage
        try:            
            final_vel = ((self.mass - t_mass) / (self.mass + t_mass)) * self.velocity + ((2 * t_mass) / (self.mass + t_mass)) * t_velocity
            if final_vel.length() != 0:
                self.target = final_vel.normalize()
        except:
            pass

    def dispose(self):
        # 화면 밖으로 벗어나게 되면 객체를 삭제, memory leak 방지
        if self.rect.x + self.rect.width + env.MARGIN < 0:
            self.kill()
        elif self.rect.x + self.rect.width - env.MARGIN >= env.WIDTH:
            self.kill()
        elif self.rect.y + self.rect.height + env.MARGIN < 0:
            self.kill()
        elif self.rect.y + self.rect.height - env.MARGIN >= env.HEIGHT:
            self.kill()

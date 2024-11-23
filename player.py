import pygame
from util import Util
from enviroment import Enviroment as env

class Player(pygame.sprite.Sprite):
    def __init__(self, main, pos, sprites, missile_sprites):
        super().__init__()
        self.sprites = sprites
        self.missile_sprites = missile_sprites
        #self.image = pygame.image.load(env.GAME_IMG_DIR + "player.png").convert_alpha()
        self.dir = 0
        self.image = self.sprites[self.dir]
        self.rect = self.image.get_rect()
        self.rect.center = pos          # 정중앙에 위치하려면 self.rect.center 값으로 설정해야함
        self.speed = 2.0                # 이동 속도 설정
        self.pos = pos
        self.move_x = 0
        self.move_y = 0
        self.target = pygame.Vector2(0, 0)
        self.velocity = self.target * self.speed
        self.mass = 1000
        self.damage = 1
        self.id = "player"

        self.collider = False
        self.collider_time = pygame.time.get_ticks()
        self.collider_delay_time = 300
        self.effect_id = "0"
        self.main = main
        
        self.health = 3
        self.total_health = 3
        
        self.shield_yn = False
        self.shield_time = 3000
        
        self.power = 1
        self.power_yn = False
        self.power_time = pygame.time.get_ticks()
        self.power_delay_time = 3000
        
        self.bomb_cnt = 3
        self.bomb_max_cnt = 7
        self.bomb_time = pygame.time.get_ticks()
        self.bomb_delay_time = 1000
    
        
        self.jewerly_cnt = 0
        self.islive = True
        
    def key_pressed(self):
        keys = pygame.key.get_pressed()
        self.move_x = 0
        self.move_y = 0
        if keys[pygame.K_a] and self.rect.x > 0:            
            self.move_x = -self.speed
            return True
        if keys[pygame.K_d] and self.rect.x + self.rect.width < env.WIDTH:            
            self.move_x = self.speed
            return True
        if keys[pygame.K_w] and self.rect.y > 0:
            self.move_y = -self.speed
            return True
        if keys[pygame.K_s] and self.rect.y + self.rect.height < env.HEIGHT:
            self.move_y = self.speed
            return True        
        if keys[pygame.K_z]:
            self.fire_bomb()                    
            
    def fire_bomb(self):
        if pygame.time.get_ticks() - self.bomb_time > self.bomb_delay_time:
            if self.bomb_cnt > 0:
                self.bomb_cnt -= 1
                self.main.fire_bomb()
                self.bomb_time = pygame.time.get_ticks()

    def move(self):
        if self.collider:
            self.velocity = self.target
            self.collider = False
        else:
            self.target = pygame.Vector2(self.move_x, self.move_y)
            self.velocity = self.target * self.speed
        
        self.pos += self.velocity
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
    def update(self):
        if self.islive:
            self.key_pressed()
            self.move()                            
            self.aimed()
            self.destroy()
        
    def destroy(self):
        if self.health <= 0:
            x = self.rect.centerx
            y = self.rect.centery
            self.main.effect.circle_explode(x, y, 50, 30)
            self.islive = False
            self.main.sound_effect.make_sound("player_explosion")
            #self.main.player_sprites.empty()
            self.kill()
        
    def aimed(self):        
        x1 = self.rect.centerx
        y1 = self.rect.centery
        x2 = self.main.crosshair.rect.centerx
        y2 = self.main.crosshair.rect.centery        
        self.dir = int(Util.pos_to_angle(x1, y1, x2, y2))
        self.image = self.sprites[self.dir]
        
    def fired(self):  
        if self.islive:  
            self.main.sound_effect.make_sound("player_bullet")    
            x3 = self.rect.centerx
            y3 = self.rect.centery
            missile = Missile(self.main, (x3, y3), self.dir, self.missile_sprites[self.dir], self.power)
            self.main.player_sprites.add(missile)
        
        if self.power_yn:
            dir1 = int(self.dir - 10 + 360) if self.dir - 10 >= 360 else self.dir - 10
            dir2 = int(self.dir + 10 - 360) if self.dir + 10 >= 360 else self.dir + 10
            missile = Missile(self.main, (x3, y3), dir1, self.missile_sprites[dir1], self.power)
            self.main.player_sprites.add(missile)
            missile = Missile(self.main, (x3, y3), dir2, self.missile_sprites[dir2], self.power)
            self.main.player_sprites.add(missile)
            
            if pygame.time.get_ticks() - self.power_time > self.power_delay_time:
                self.power_yn = False

    def bomb_up(self):
        if self.bomb_cnt < self.bomb_max_cnt:
            self.bomb_cnt += 1
            
    def jewerly_up(self):
        self.main.total_jewerly_cnt += 5
    
    def health_up(self):
        if self.total_health < self.health:
            self.health += 1
    
    def power_up(self):
        self.power_yn = True
        self.power_time = pygame.time.get_ticks()
        
    def create_shield(self):
        if not(self.shield_yn):
            self.shield_yn = True
            shield = Shield(self.pos, self.main, self.shield_time)  
            self.main.player_sprites.add(shield)
    
    def handle_collision(self, t_velocity, t_mass, damage = 0):
        if pygame.time.get_ticks() - self.collider_time > self.collider_delay_time:
            self.health -= damage
            self.collider = True
            final_vel = ((self.mass - t_mass) / (self.mass + t_mass)) * self.velocity + ((2 * t_mass) / (self.mass + t_mass)) * t_velocity
            if final_vel.length() != 0:
                self.target = final_vel.normalize()

            self.collider_time = pygame.time.get_ticks()

class Shield(pygame.sprite.Sprite):
    def __init__(self, pos, main, shield_time):
        super().__init__()
        self.image = pygame.image.load(env.GAME_IMG_DIR + "player_shield.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.id = "player_shield"
        self.effect_id = "0"
        self.group_id = "player"
        self.shield_time = pygame.time.get_ticks()
        self.shield_delay_time = shield_time
        self.speed = 0
        self.mass = 1000
        self.target = pygame.Vector2(0, 0)
        self.velocity = self.target * self.speed
        self.main = main
        self.damage = 0
                
    def update(self):
        self.pos = self.main.player.pos
        self.rect.center = self.pos
        
        if pygame.time.get_ticks() - self.shield_time > self.shield_delay_time:
            self.main.player.shield_yn = False
            self.kill()
            
        if not(self.main.player.islive):
            self.kill()
        
    def handle_collision(self, t_velocity, t_mass, damage):
        pass

class CrossHair(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(env.GAME_IMG_DIR + "crosshair.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.id = "crosshair"
        self.group_id = "player"
                
    def update(self):
        x, y = pygame.mouse.get_pos()
        self.rect.center = (x, y)        

class Missile(pygame.sprite.Sprite):
    def __init__(self, main, pos, dir, image, power):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos
        self.dir = dir        
        self.target = pygame.Vector2(env.ANGLE_TO_VECTORS[self.dir])
        self.id = "missile"
        self.group_id = "player"
        self.effect_id = "0"
        self.speed = 10
        self.mass = 3
        self.main = main
        self.damage = power
                
    def update(self):        
        self.move()
        self.dispose()
        
    def move(self):
        self.velocity = self.target * self.speed        
        self.pos += self.velocity
        self.rect.center = self.pos  
        
    def handle_collision(self, t_velocity, t_mass, damage):
        x = self.rect.centerx
        y = self.rect.centery
        self.main.effect.circle_explode(x, y, 25, 8)
        self.main.sound_effect.make_sound("collision")
        self.kill()
    
    def dispose(self):
        if self.rect.x + self.rect.width < 0:
            self.kill()
        elif self.rect.x + self.rect.width >= env.WIDTH:
            self.kill()
        elif self.rect.y + self.rect.height < 0:
            self.kill()
        elif self.rect.y + self.rect.height >= env.HEIGHT:
            self.kill()


import pygame
import random
from enviroment import Enviroment as env
from effect import Effect

class Collider():
    def __init__(self):
        self.collision_check_list = []

    def add_sprites(self, sprites):
        for sprite in sprites.sprites():
            self.collision_check_list.append(sprite)        

    def check_collision(self, main):
        #self.collision_check_list.append(self.player_sprites.sprites()[0])
        #self.collision_check_list.append(player)
        
        # for sprite in meteor_sprites.sprites():
        #     self.collision_check_list.append(sprite)
        
        # Sweep and Prone 알고리즘
        # x축만 정렬
        self.collision_check_list.sort(key=lambda sprite: sprite.rect.x)

        for i in range(len(self.collision_check_list)):
            sprite_a = self.collision_check_list[i]
            for j in range(i + 1, len(self.collision_check_list)):
                sprite_b = self.collision_check_list[j]
                if sprite_a.rect.x + sprite_a.rect.width < 0 or sprite_a.rect.x > env.WIDTH:
                    break

                if sprite_a.rect.x + sprite_a.rect.width < sprite_b.rect.x:
                    break
                
                if sprite_a.id == "player" and sprite_b.id == "missile" or \
                    sprite_b.id == "player" and sprite_a.id == "missile" or \
                    sprite_a.id == "missile" and sprite_b.id == "missile" or \
                    sprite_b.id == "missile" and sprite_a.id == "missile" or \
                    sprite_a.id == "missile" and sprite_b.id == "player_shield" or \
                    sprite_b.id == "missile" and sprite_a.id == "player_shield" or \
                    sprite_a.id == "missile" and sprite_b.id == "item" or \
                    sprite_b.id == "missile" and sprite_a.id == "item" or \
                    sprite_a.id == "enemy" and sprite_b.id == "item" or \
                    sprite_b.id == "enemy" and sprite_a.id == "item" or \
                    sprite_a.id == "item" and sprite_b.id == "item" or \
                    sprite_b.id == "item" and sprite_a.id == "item" :
                        break

                if sprite_a.rect.x <= sprite_b.rect.x and sprite_a.rect.x + sprite_a.rect.width >= sprite_b.rect.x:
                    collide_pos = pygame.sprite.collide_mask(sprite_a, sprite_b)
                    if collide_pos:
                        sprite_a.handle_collision(sprite_b.velocity, sprite_b.mass, sprite_b.damage)
                        sprite_b.handle_collision(sprite_a.velocity, sprite_a.mass, sprite_a.damage)
                        x = sprite_a.rect.x + collide_pos[0]
                        y = sprite_a.rect.y + collide_pos[1]
                        cnt = random.randint(15, 30)
                        
                        if sprite_a.id == "enemy":
                            main.effect.radial_explode(sprite_a.effect_id, x, y, 5, cnt)
                        elif sprite_a.id == "player":
                            main.effect.radial_explode(sprite_a.effect_id, x, y, 3, cnt)

                        cnt = random.randint(15, 30)
                        if sprite_b.id == "enemy":
                            main.effect.radial_explode(sprite_b.effect_id, x, y, 5, cnt)
                        elif sprite_b.id == "player":
                            main.effect.radial_explode(sprite_a.effect_id, x, y, 3, cnt)

        self.collision_check_list.clear()
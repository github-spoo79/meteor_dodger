import pygame
import random
from enviroment import Enviroment as env
from meteor import Meteor
from util import Util


class Spawn():
    def __init__(self):
        self.meteor_spawn_delay_time = 250 # 운석 delay time 0.5초 (1000 = 1초)
        self.meteor_spawn_time = pygame.time.get_ticks()
        
    def spawn_meteor(self, main):
        #0.5초마다 한개씩 생성
        if pygame.time.get_ticks() - self.meteor_spawn_time > self.meteor_spawn_delay_time:
            dir = random.randint(1, 4)
            if dir == env.TOP:
                pos = (random.randint(0, env.WIDTH), 0)
            elif dir == env.RIGHT:
                pos = (env.WIDTH, random.randint(0, env.HEIGHT))
            elif dir == env.BOTTOM:
                pos = (random.randint(0, env.WIDTH), env.HEIGHT)
            else:
                pos = (0, random.randint(0, env.HEIGHT))

            if Util.is_probability(env.METEOR_DIR_CHANCE):
                if dir == env.TOP:
                    d_pos = (pos[0], env.HEIGHT)
                elif dir == env.RIGHT:
                    d_pos = (0, pos[1])
                elif dir == env.BOTTOM:
                    d_pos = (pos[0], 0)
                else:
                    d_pos = (env.WIDTH, pos[1])                
            else:
                d_pos = (main.player.rect.centerx, main.player.rect.centery)

            meteor_type = random.choice(['A', 'B'])
            meteor_color = random.choice(['1', '2', '3', '4'])
            meteor_size  = random.randint(10, 49)
            r = main.resources.get_meteor(meteor_type, meteor_color)
            
            # 운석의 크기에 따라서 무게를 다르게 설정
            # print("1:{0}".format(pos))
            meteor = Meteor(pos, d_pos, r[meteor_size], meteor_size, meteor_color)
            main.meteor_sprites.add(meteor)
            
            self.meteor_spawn_time = pygame.time.get_ticks() #spawn 시간 현재시간으로 초기화
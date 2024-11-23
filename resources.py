import pygame
from util import Util
from enviroment import Enviroment as env

class Resources:
    def __init__(self):
        self.player = [] # player sprites
        self.missile = [] # missile sprites
        self.bomb_item = pygame.image.load(env.GAME_IMG_DIR + "bomb_item.png").convert_alpha()
        self.item_shield = pygame.image.load(env.GAME_IMG_DIR + "item_shield.png").convert_alpha()
        self.item_power = pygame.image.load(env.GAME_IMG_DIR + "item_power.png").convert_alpha()
        self.item_jewerly = pygame.image.load(env.GAME_IMG_DIR + "item_jewerly.png").convert_alpha()
        self.item_energy = pygame.image.load(env.GAME_IMG_DIR + "item_energy.png").convert_alpha()
        self.item_bomb = pygame.image.load(env.GAME_IMG_DIR + "item_bomb.png").convert_alpha()
        self.digit_font_48 = pygame.font.Font(env.GAME_FONT_DIR + "DS-DIGIT.ttf", 48)
        self.digit_font_32 = pygame.font.Font(env.GAME_FONT_DIR + "DS-DIGIT.ttf", 32)
        self.galmuri_font_45 = pygame.font.Font(env.GAME_FONT_DIR + "Galmuri14.ttf", 45)
        self.galmuri_font_45.set_bold(True)
        self.galmuri_font_35 = pygame.font.Font(env.GAME_FONT_DIR + "Galmuri14.ttf", 35)
        self.galmuri_font_35.set_bold(True)
        self.galmuri_font_30 = pygame.font.Font(env.GAME_FONT_DIR + "Galmuri14.ttf", 30)
        self.galmuri_font_30.set_bold(True)
        self.galmuri_font_20 = pygame.font.Font(env.GAME_FONT_DIR + "Galmuri14.ttf", 20)
        self.galmuri_font_20.set_bold(True)
        self.galmuri_font_15 = pygame.font.Font(env.GAME_FONT_DIR + "Galmuri14.ttf", 15)
        self.galmuri_font_15.set_bold(True)
        
        self.meteorA1 = [[] for _ in range(env.METEOR_SIZE + 1)]
        self.meteorB1 = [[] for _ in range(env.METEOR_SIZE + 1)]
        self.meteorA2 = [[] for _ in range(env.METEOR_SIZE + 1)]
        self.meteorB2 = [[] for _ in range(env.METEOR_SIZE + 1)]
        self.meteorA3 = [[] for _ in range(env.METEOR_SIZE + 1)]
        self.meteorB3 = [[] for _ in range(env.METEOR_SIZE + 1)]
        self.meteorA4 = [[] for _ in range(env.METEOR_SIZE + 1)]
        self.meteorB4 = [[] for _ in range(env.METEOR_SIZE + 1)]

        self.effect0 = [] # main character effect RED
        self.effect1 = []
        self.effect2 = []
        self.effect3 = []
        self.effect4 = []
        
        self.explosion0 = [] #white explosion 
        self.explosion1 = [] #red
        self.explosion2 = [] #orange
        self.explosion3 = [] #yellow
        self.render()


    def render(self):
        effect0_image = pygame.Surface((env.EFFECT_DEFAULT_SIZE, env.EFFECT_DEFAULT_SIZE))
        effect0_image.fill(env.EFFECT_01_COLOR)
        pygame.draw.rect(effect0_image, env.EFFECT_00_COLOR, effect0_image.get_rect())

        effect1_image = pygame.Surface((env.EFFECT_DEFAULT_SIZE, env.EFFECT_DEFAULT_SIZE))
        effect1_image.fill(env.EFFECT_01_COLOR)
        pygame.draw.rect(effect1_image, env.EFFECT_01_COLOR, effect1_image.get_rect())

        effect2_image = pygame.Surface((env.EFFECT_DEFAULT_SIZE, env.EFFECT_DEFAULT_SIZE))
        effect2_image.fill(env.EFFECT_02_COLOR)
        pygame.draw.rect(effect2_image, env.EFFECT_02_COLOR, effect2_image.get_rect())

        effect3_image = pygame.Surface((env.EFFECT_DEFAULT_SIZE, env.EFFECT_DEFAULT_SIZE))
        effect3_image.fill(env.EFFECT_03_COLOR)
        pygame.draw.rect(effect3_image, env.EFFECT_03_COLOR, effect3_image.get_rect())

        effect4_image = pygame.Surface((env.EFFECT_DEFAULT_SIZE, env.EFFECT_DEFAULT_SIZE))
        effect4_image.fill(env.EFFECT_04_COLOR)
        pygame.draw.rect(effect4_image, env.EFFECT_04_COLOR, effect4_image.get_rect())

        for i in range(env.EFFECT_DEFAULT_SIZE + 1):
            self.effect0.append(Util.resize_image(effect0_image, i))
            self.effect1.append(Util.resize_image(effect1_image, i))
            self.effect2.append(Util.resize_image(effect2_image, i))
            self.effect3.append(Util.resize_image(effect3_image, i))
            self.effect4.append(Util.resize_image(effect4_image, i))

        a1_image = pygame.image.load(env.GAME_IMG_DIR + "meteor_01_A.png").convert_alpha()
        b1_image = pygame.image.load(env.GAME_IMG_DIR + "meteor_01_B.png").convert_alpha()
        a2_image = pygame.image.load(env.GAME_IMG_DIR + "meteor_02_A.png").convert_alpha()
        b2_image = pygame.image.load(env.GAME_IMG_DIR + "meteor_02_B.png").convert_alpha()
        a3_image = pygame.image.load(env.GAME_IMG_DIR + "meteor_03_A.png").convert_alpha()
        b3_image = pygame.image.load(env.GAME_IMG_DIR + "meteor_03_B.png").convert_alpha()
        a4_image = pygame.image.load(env.GAME_IMG_DIR + "meteor_04_A.png").convert_alpha()
        b4_image = pygame.image.load(env.GAME_IMG_DIR + "meteor_04_B.png").convert_alpha()
        
        for i in range(env.METEOR_SIZE + 1):
            Util.rotates(Util.resize_image(a1_image, i), self.meteorA1[i] , env.DEFAULT_ANGLE)
            Util.rotates(Util.resize_image(b1_image, i), self.meteorB1[i] , env.DEFAULT_ANGLE)
            Util.rotates(Util.resize_image(a2_image, i), self.meteorA2[i] , env.DEFAULT_ANGLE)
            Util.rotates(Util.resize_image(b2_image, i), self.meteorB2[i] , env.DEFAULT_ANGLE)
            Util.rotates(Util.resize_image(a3_image, i), self.meteorA3[i] , env.DEFAULT_ANGLE)
            Util.rotates(Util.resize_image(b3_image, i), self.meteorB3[i] , env.DEFAULT_ANGLE)
            Util.rotates(Util.resize_image(a4_image, i), self.meteorA4[i] , env.DEFAULT_ANGLE)
            Util.rotates(Util.resize_image(b4_image, i), self.meteorB4[i] , env.DEFAULT_ANGLE)
            
        explosion0_image = pygame.image.load(env.GAME_IMG_DIR + "explosion.png").convert_alpha()
        explosion1_image = Util.transfer_color(explosion0_image, (255, 0, 0))
        explosion2_image = Util.transfer_color(explosion0_image, (255, 165, 0))
        explosion3_image = Util.transfer_color(explosion0_image, (255, 255, 0))
        for i in range(env.METEOR_SIZE + 1):
            self.explosion0.append(Util.resize_image(explosion0_image, i))
            self.explosion1.append(Util.resize_image(explosion1_image, i))
            self.explosion2.append(Util.resize_image(explosion2_image, i))
            self.explosion3.append(Util.resize_image(explosion3_image, i))
            
        player_image = pygame.image.load(env.GAME_IMG_DIR + "player.png").convert_alpha()
        Util.rotates(player_image, self.player, env.DEFAULT_ANGLE)
        
        missile_image = pygame.image.load(env.GAME_IMG_DIR + "missile.png").convert_alpha()
        Util.rotates(missile_image, self.missile, env.DEFAULT_ANGLE)
            

    def get_meteor(self, type, color):
        # 속성 이름을 동적으로 조합
        attr_name = f'meteor{type}{color}'
        return getattr(self, attr_name)
    
    def get_effect(self, color):
        attr_name = f'effect{color}'
        return getattr(self, attr_name)


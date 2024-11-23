import pygame
import sys
import time
import os
from enviroment import Enviroment as env
from player import Player, CrossHair
from spawn import Spawn
from background import Background
from resources import Resources
from collider import Collider
from effect import Effect
from sound import Music, SoundEffect
from util import Util
from menu import Title, Setting, Upgrade

class Main():
    def __init__(self):        
        pygame.init()        
        pygame.mixer.init()
        pygame.mixer.set_num_channels(env.MAX_MIXER_CHANNEL)
        self.screen = pygame.display.set_mode((env.WIDTH, env.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True 
        self.grab = True
        
        pygame.display.set_caption(env.GAME_TITLE)
        icon = pygame.image.load(env.GAME_DIR + "/meteor_dodger.ico")
        pygame.display.set_icon(icon)

        self.meteor_sprites = pygame.sprite.Group() # 운석 sprites group 생성
        self.effect_sprites = pygame.sprite.Group() # effect sprites group 생성
        self.item_sprites = pygame.sprite.Group()   # item sprites group 생성
        self.player_sprites = pygame.sprite.Group()
        self.crosshair_sprites = pygame.sprite.Group()
        
        self.data = Util.load_prperties(env.GAME_DIR + "/config.ini")
        
        self.background = Background()
        self.resources = Resources()
        self.collider = Collider()
        self.effect = Effect(self)
        self.music = Music()
        self.sound_effect = SoundEffect()
        self.music.play()
        
        self.title = Title(self)
        self.setting = Setting(self)
        self.upgrade = Upgrade(self)

        self.GAME_STATE = env.TITLE
        self.ANSWER_INDEX = 0
       
        self.time = 0
        self.bomb_cnt = 0
        self.jewerly_cnt = 0
        self.total_jewerly_cnt = 0
        self.time_record = 0                         

        self.total_jewerly_cnt = int(self.data["jewerly_cnt"])       

        
    def init(self):
        self.meteor_sprites.empty()
        self.effect_sprites.empty()
        self.item_sprites.empty()
        
        self.spawn = Spawn()
        self.crosshair = CrossHair((env.START_POS_X, env.START_POS_Y))
        self.player = Player(self, (env.START_POS_X, env.START_POS_Y), self.resources.player, self.resources.missile) 
        self.player_sprites.add(self.player)
        self.crosshair_sprites.add(self.crosshair)
        self.player.health = int(self.data["health"])
        self.player.total_health = int(self.data["health"])
        self.player.bomb_cnt = int(self.data["bomb"])
        self.player.power = int(self.data["power"])
        self.player.shield_time = int(self.data["shield_time"]) * 1000
        self.player.power_delay_time = int(self.data["power_time"]) * 1000
        self.total_jewerly_cnt = int(self.data["jewerly_cnt"])        
        
    def state(self):
        if self.GAME_STATE == env.TITLE:
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False) #마우스를 스크린 안에 고정 처리
            self.title.running = True
            self.title.play()
        elif self.GAME_STATE == env.PLAYING:
            pygame.mouse.set_visible(False)
            pygame.event.set_grab(True) #마우스를 스크린 안에 고정 처리
            self.running = True
            self.init()
            self.play()
        elif self.GAME_STATE == env.SETTING:            
            self.setting.running = True
            self.setting.play()            
        elif self.GAME_STATE == env.UPGRADE:
            self.upgrade.running = True
            self.upgrade.play()
        elif self.GAME_STATE == env.TRYAGAIN:
            self.GAME_STATE = env.PLAYING
            self.init()
            self.play()        
        elif self.GAME_STATE == env.QUIT:
            pygame.quit()
            sys.exit(0)
        
    def play(self):
        start_time = time.time()
        while self.running:
            if self.player.islive:
                current_time = time.time() - start_time
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.player.fired()                     
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.set_grab()             
                    elif event.key == pygame.K_DOWN:
                        self.sound_effect.make_sound("menu_bar")
                        self.ANSWER_INDEX = (self.ANSWER_INDEX + 1) % 2
                    elif event.key == pygame.K_UP:
                        self.sound_effect.make_sound("menu_bar")
                        self.ANSWER_INDEX = (self.ANSWER_INDEX - 1 + 2) % 2
                    elif event.key == pygame.K_RIGHT:
                        self.sound_effect.make_sound("menu_bar")
                        self.ANSWER_INDEX = (self.ANSWER_INDEX + 1) % 2
                    elif event.key == pygame.K_LEFT:
                        self.sound_effect.make_sound("menu_bar")
                        self.ANSWER_INDEX = (self.ANSWER_INDEX - 1 + 2) % 2
                    elif event.key == pygame.K_RETURN:
                        self.try_again_process()

            self.item_sprites.update()
            self.player_sprites.update()     
            self.meteor_sprites.update(self)
            self.effect_sprites.update()
            self.crosshair_sprites.update()

            self.spawn.spawn_meteor(self)

            self.collider.add_sprites(self.player_sprites)
            self.collider.add_sprites(self.meteor_sprites)
            self.collider.add_sprites(self.item_sprites)
            self.collider.check_collision(self)

            self.screen.fill(env.BLACK)
            self.background.draw(self.screen)
            self.item_sprites.draw(self.screen)
            self.player_sprites.draw(self.screen)
            self.meteor_sprites.draw(self.screen)
            self.effect_sprites.draw(self.screen)
            self.crosshair_sprites.draw(self.screen)
            
            self.bomb_item()
            self.energy_bar()
            self.timer(current_time)
            self.total_jewerly()
            if not(self.player.islive):
                self.show_tryagain()

            pygame.display.flip()
            self.clock.tick(env.FPS)
            
    def bomb_item(self):
        image = self.resources.bomb_item 
        for i in range(self.player.bomb_cnt):            
            self.screen.blit(image, (env.BOMB_ITEM_X + (env.BOMB_ITEM_MARGIN * i), env.BOMB_ITEM_Y))            
            
    def energy_bar(self):   
        x  = int((155 * self.player.health) / self.player.total_health)
        bar = pygame.Rect(env.BAR_X, env.BAR_Y, env.BAR_WIDTH, env.BAR_HEIGHT)
        energy = pygame.Rect(env.BAR_X, env.BAR_Y, x, env.BAR_HEIGHT)
        pygame.draw.rect(self.screen, env.RED, bar)
        pygame.draw.rect(self.screen, env.YELLOW, energy)
        pygame.draw.rect(self.screen, env.WHITE, bar, 1)
        
    def fire_bomb(self):
        for meteor in self.meteor_sprites:
            meteor.destroy(self)
        
    def total_jewerly(self):
        jewerly_text = f"{self.total_jewerly_cnt}"
        text = self.resources.digit_font_32.render(jewerly_text, True, env.WHITE)             
        text_rect = text.get_rect()
        text_rect.right = 790 
        text_rect.top = 5
        self.screen.blit(text, text_rect)
        
        image = self.resources.item_jewerly
        image_left = text_rect.left - (self.resources.item_jewerly.get_rect().width + 5)
        self.screen.blit(image, (image_left, 10))        
    
    def timer(self, microseconds):
        time_text = f"{microseconds:.2f}"  # 밀리초 단위로 표시
        text = self.resources.digit_font_48.render(time_text, True, env.WHITE)             
        text_rect = text.get_rect()
        text_rect.left = 360
        text_rect.top = 5
        self.screen.blit(text, text_rect)
        
    def set_grab(self):
        self.grab = not(self.grab)
        pygame.event.set_grab(self.grab)
        
    def save_data(self):
        Util.save_prperties(env.GAME_DIR + "/config.ini", self.data)
            
    def show_tryagain(self):
        self.data["jewerly_cnt"] = self.total_jewerly_cnt
        self.save_data()
        ask_text = "Try again?"
        Util.print_text(self, ask_text, 400, 300, "MIDDLE", env.WHITE, env.CENTER, True)
        self.show_anwser()
            
    def show_anwser(self):
        answer_text = ["Yes", "No"]
        margin = 160
        text_color = env.WHITE
        for i in range(len(answer_text)):
            if self.ANSWER_INDEX == i:
                text_color = env.YELLOW
            else:
                text_color = env.WHITE

            Util.print_text(self, answer_text[i], 320 + (margin * i), 380 , "MIDDLE", text_color, env.CENTER, True)        
            
    def try_again_process(self):
        if not(self.player.islive):
            if self.ANSWER_INDEX == 0:
                self.running_menu = True
                self.GAME_STATE = env.TRYAGAIN
                self.state()
            
            elif self.ANSWER_INDEX == 1:
                self.running = False
                self.running_menu = True
                self.GAME_STATE = env.TITLE
                self.state()
               
if __name__ == "__main__":    
    gameMain = Main()
    gameMain.state()
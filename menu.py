import pygame
from util import Util
from enviroment import Enviroment as env

class Title():
    def __init__(self, main):
        self.main = main
        self.MENU_INDEX = 0        
        self.running = True
    
    def play(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.main.sound_effect.make_sound("menu_bar")
                        self.MENU_INDEX = (self.MENU_INDEX + 1) % 4
                    elif event.key == pygame.K_UP:
                        self.main.sound_effect.make_sound("menu_bar")
                        self.MENU_INDEX = (self.MENU_INDEX - 1 + 4) % 4
                    elif event.key == pygame.K_RIGHT:
                        self.main.sound_effect.make_sound("menu_bar")
                        self.MENU_INDEX = (self.MENU_INDEX + 1) % 4
                    elif event.key == pygame.K_LEFT:
                        self.main.sound_effect.make_sound("menu_bar")
                        self.MENU_INDEX = (self.MENU_INDEX - 1 + 4) % 4                        
                    elif event.key == pygame.K_RETURN:
                        self.menu_process()
            
            self.main.screen.fill(env.BLACK)           
            self.main.background.draw(self.main.screen)
            self.show_title()
            self.main.total_jewerly()
            pygame.display.flip()
            self.main.clock.tick(env.FPS)
            
    def show_title(self):
        title_text = env.GAME_TITLE
        Util.print_text(self.main, title_text, 400, 150, "LARGE", env.WHITE, env.CENTER, True)
        self.show_menu()
                
    def show_menu(self):
        menu_text = ["Game Start", "Upgrade", "Setting", "Exit"]        
        margin = 65
        text_color = env.WHITE
        for i in range(len(menu_text)):
            if self.MENU_INDEX == i:
                text_color = env.YELLOW
            else:
                text_color = env.WHITE
                                
            Util.print_text(self.main, menu_text[i], 400, 500 + (margin * i), "MIDDLE2", text_color, env.CENTER, True)
            
    def menu_process(self):
        self.running = False
        if self.MENU_INDEX == 0:
            self.main.GAME_STATE = env.PLAYING
        
        elif self.MENU_INDEX == 1:
            self.main.GAME_STATE = env.UPGRADE
            
        elif self.MENU_INDEX == 2:
            self.main.GAME_STATE = env.SETTING
        else:
            self.main.GAME_STATE = env.QUIT        
        self.main.state()
        
class Setting():
    def __init__(self, main):
        self.running = True
        self.SETTING_INDEX = 0
        self.main = main
    
    def play(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.main.sound_effect.make_sound("menu_bar")
                        self.SETTING_INDEX = (self.SETTING_INDEX + 1) % 3
                    elif event.key == pygame.K_UP:
                        self.main.sound_effect.make_sound("menu_bar")
                        self.SETTING_INDEX = (self.SETTING_INDEX - 1 + 3) % 3
                    elif event.key == pygame.K_RIGHT:
                        self.main.sound_effect.make_sound("menu_bar")
                        self.SETTING_INDEX = (self.SETTING_INDEX + 1) % 3
                    elif event.key == pygame.K_LEFT:
                        self.main.sound_effect.make_sound("menu_bar")
                        self.SETTING_INDEX = (self.SETTING_INDEX - 1 + 3) % 3
                    elif event.key == pygame.K_RETURN:
                        self.setting_process()
            
            self.main.screen.fill(env.BLACK)           
            self.main.background.draw(self.main.screen)
            self.show_setting()
            self.main.total_jewerly()
            pygame.display.flip()
            
            self.main.clock.tick(env.FPS)
            
    def show_setting(self):
        setting_text = ["Sound", "Effect", "Return To Main"]
        setting_value = [self.main.music.ing, self.main.sound_effect.ing, ""]
        margin = 65
        text_color = env.WHITE
        for i in range(len(setting_text)):
            if self.SETTING_INDEX == i:
                text_color = env.YELLOW
            else:
                text_color = env.WHITE                            
                            
            if setting_value[i]:
                text = "ON"
            elif setting_value[i] == "":
                text = ""
            else:
                text = "OFF"                
            Util.print_text(self.main, setting_text[i], 250, 500 + (margin * i), "MIDDLE2", text_color, env.LEFT, True)
            Util.print_text(self.main, text, 400, 500 + (margin * i), "MIDDLE2", text_color, env.LEFT, True)
            
    def setting_process(self):
        if self.SETTING_INDEX == 2:
            self.main.GAME_STATE = env.TITLE
            self.running = False
            
        elif self.SETTING_INDEX == 0:
            self.main.music.ing = not(self.main.music.ing)        
            if self.main.music.ing:
                self.main.music.play()
            else:
                self.main.music.stop()
                
        elif self.SETTING_INDEX == 1:
            self.main.sound_effect.ing = not(self.main.sound_effect.ing)
        
        self.main.state()
        
class Upgrade():
    def __init__(self, main):
        self.running = True
        self.main = main
        self.UPGRADE_INDEX = 0        
        self.more_jewelry = 0
        self.show_warning = False
        
        self.health = int(self.main.data["health"])
        self.power = int(self.main.data["power"])
        self.bomb = int(self.main.data["bomb"])
        self.shield_time = int(self.main.data["shield_time"])
        self.power_time = int(self.main.data["power_time"])
        
        self.health_max = int(self.main.data["health_max"])
        self.bomb_max = int(self.main.data["bomb_max"])
        self.power_max = int(self.main.data["power_max"])
        self.shield_time_max = int(self.main.data["shield_time_max"])
        self.power_time_max = int(self.main.data["power_time_max"])
        
        self.health_jewerly = int(self.main.data["health_jewerly"])
        self.bomb_jewerly = int(self.main.data["bomb_jewerly"])
        self.power_jewerly = int(self.main.data["power_jewerly"])
        self.shield_time_jewerly = int(self.main.data["shield_time_jewerly"])
        self.power_time_jewerly = int(self.main.data["power_time_jewerly"])
        
    def play(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.main.sound_effect.make_sound("menu_bar")
                        self.UPGRADE_INDEX = (self.UPGRADE_INDEX + 1) % 6
                    elif event.key == pygame.K_UP:
                        self.main.sound_effect.make_sound("menu_bar")
                        self.UPGRADE_INDEX = (self.UPGRADE_INDEX - 1 + 6) % 6
                    elif event.key == pygame.K_RIGHT:
                        self.main.sound_effect.make_sound("menu_bar")
                        self.UPGRADE_INDEX = (self.UPGRADE_INDEX + 1) % 6
                    elif event.key == pygame.K_LEFT:
                        self.main.sound_effect.make_sound("menu_bar")
                        self.UPGRADE_INDEX = (self.UPGRADE_INDEX - 1 + 6) % 6
                    elif event.key == pygame.K_RETURN:
                        self.upgrade_process()
            
            self.main.screen.fill(env.BLACK)           
            self.main.background.draw(self.main.screen)
            self.show_upgrade()
            if self.show_warning:
                self.warning(str(self.more_jewelry))
            self.main.total_jewerly()
            pygame.display.flip()
            
            self.main.clock.tick(env.FPS)
            
    def warning(self, jewerly):        
        message = f"Not enough jewerly... You need more {jewerly} jewerly."
        Util.print_text(self.main, message, 400, 200, "MIDDLE3", env.RED, env.CENTER, False)

    def show_upgrade(self):
        upgrade_text = ["Health", "Missile Power", "Bomb Count", "Shield Time", "Power Time", "Return To Main"]
        upgrade_value = [self.main.data["health"], self.main.data["power"], self.main.data["bomb"], self.main.data["shield_time"], self.main.data["power_time"], 0]
        upgrade_jewerly = [self.health_jewerly, self.power_jewerly, self.bomb_jewerly, self.shield_time_jewerly, self.power_time_jewerly, 0]
        
        margin = 65
        text_color = env.WHITE
        for i in range(len(upgrade_text)):
            if self.UPGRADE_INDEX == i:
                text_color = env.YELLOW
            else:
                text_color = env.WHITE                            

            if i == len(upgrade_text) - 1:                
                Util.print_text(self.main, "Return To Main", 400, 700, "MIDDLE2", text_color, env.CENTER, True)                            
            else:
                Util.print_text(self.main, upgrade_text[i], 100, 350 + (margin * i), "MIDDLE2", text_color, env.LEFT, True)                
                for j in range(10):
                    if int(upgrade_value[i]) - 1 < j:
                        Util.print_text(self.main, "□", 350 + (j * 30), 350 + (margin * i), "MIDDLE2", text_color, env.LEFT, True)
                    else:
                        Util.print_text(self.main, "■", 350 + (j * 30), 350 + (margin * i), "MIDDLE2", text_color, env.LEFT, True)
                        
                Util.print_text(self.main, str(upgrade_jewerly[i]), 680, 350 + (margin * i), "MIDDLE2", text_color, env.LEFT, True)


    def upgrade_process(self):
        if self.UPGRADE_INDEX == 0:
            self.upgrade_data("health")
            
        elif self.UPGRADE_INDEX == 1:
            self.upgrade_data("missile_power")
            
        elif self.UPGRADE_INDEX == 2:
            self.upgrade_data("bomb")
            
        elif self.UPGRADE_INDEX == 3:
            self.upgrade_data("shield_time")

        elif self.UPGRADE_INDEX == 4:
            self.upgrade_data("power_time")
            
        else:
            self.main.GAME_STATE = env.TITLE
            self.running = False

        self.main.state()
        
    def upgrade_data(self, flag):
        if flag == "health":
            if self.main.total_jewerly_cnt >= self.health_jewerly:
                if self.health_max > self.health:
                    self.health += 1
                    self.main.data["health"] = self.health
                    self.main.total_jewerly_cnt -= self.health_jewerly
                    self.main.data["jewerly_cnt"] = self.main.total_jewerly_cnt
                    self.health_jewerly += 10
                    self.main.data["health_jewerly"] = self.health_jewerly
                    self.main.save_data()
                    self.show_warning = False
            else:
                self.show_warning = True
                self.more_jewelry = int(self.health_jewerly)
        elif flag == "missile_power":
            if self.main.total_jewerly_cnt >= self.power_jewerly:
                if self.power_max > self.power:
                    self.power += 1
                    self.main.data["power"] = self.power
                    self.main.total_jewerly_cnt -= self.health_jewerly
                    self.main.data["jewerly_cnt"] = self.main.total_jewerly_cnt
                    self.power_jewerly += 10
                    self.main.data["power_jewerly"] = self.power_jewerly
                    self.main.save_data()
                    self.show_warning = False
            else:
                self.show_warning = True
                self.more_jewelry = int(self.power_jewerly)
        elif flag == "bomb":
            if self.main.total_jewerly_cnt >= self.bomb_jewerly:
                if self.bomb_max > self.bomb:
                    self.bomb += 1
                    self.main.data["bomb"] = self.bomb
                    self.main.total_jewerly_cnt -= self.bomb_jewerly
                    self.main.data["jewerly_cnt"] = self.main.total_jewerly_cnt
                    self.bomb_jewerly += 10
                    self.main.data["bomb_jewerly"] = self.bomb_jewerly
                    self.main.save_data()
                    self.show_warning = False
            else:
                self.show_warning = True
                self.more_jewelry = int(self.bomb_jewerly)
        elif flag == "shield_time":
            if self.main.total_jewerly_cnt >= self.shield_time_jewerly:
                if self.shield_time_max > self.shield_time:
                    self.shield_time += 1
                    self.main.data["shield_time"] = self.shield_time
                    self.main.total_jewerly_cnt -= self.shield_time_jewerly
                    self.main.data["jewerly_cnt"] = self.main.total_jewerly_cnt
                    self.shield_time_jewerly += 10
                    self.main.data["shield_time_jewerly"] = self.shield_time_jewerly
                    self.main.save_data()
                    self.show_warning = False
            else:
                self.show_warning = True
                self.more_jewelry = int(self.shield_time_jewerly)
        elif flag == "power_time":
            if self.main.total_jewerly_cnt >= self.power_time_jewerly:
                if self.power_time_max > self.power_time:
                    self.power_time += 1
                    self.main.data["power_time"] = self.power_time
                    self.main.total_jewerly_cnt -= self.power_time_jewerly
                    self.main.data["jewerly_cnt"] = self.main.total_jewerly_cnt
                    self.power_time_jewerly += 10
                    self.main.data["power_time_jewerly"] = self.power_time_jewerly
                    self.main.save_data()
                    self.show_warning = False
            else:
                self.show_warning = True
                self.more_jewelry = int(self.power_time_jewerly)
        else:
            pass
        
      
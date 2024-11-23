import pygame
from enviroment import Enviroment as env

class Music():
    def __init__(self):
        self.ing = True
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.load(env.GAME_SOUND_DIR + "bgm.ogg")
        
    def play(self):
        if self.ing:
            pygame.mixer.music.play(-1)
            
    def stop(self):
        pygame.mixer.music.stop()
        
    
class SoundEffect():
    def __init__(self):
        self.channel_list = []
        self.ing = True
        self.volume = 0.1
        self.collision_effect = pygame.mixer.Sound(env.GAME_SOUND_DIR + "collision.wav")
        self.enemy_explosion_effect = pygame.mixer.Sound(env.GAME_SOUND_DIR + "explosion.wav")
        self.player_bullet_effect = pygame.mixer.Sound(env.GAME_SOUND_DIR + "player_bullet.wav")
        self.player_explosion_effect = pygame.mixer.Sound(env.GAME_SOUND_DIR + "player_explosion.wav")
        self.player_jewerly_effect = pygame.mixer.Sound(env.GAME_SOUND_DIR + "player_jewerly.wav")
        self.player_upgrade_effect = pygame.mixer.Sound(env.GAME_SOUND_DIR + "player_upgrade.wav")
        self.menu_bar_effect = pygame.mixer.Sound(env.GAME_SOUND_DIR + "menu_bar.wav")

        for i in range(env.MAX_MIXER_CHANNEL):
            self.channel_list.append(pygame.mixer.Channel(i))
            
    def get_channel(self):
        for i in range(env.MAX_MIXER_CHANNEL):
            channel = self.channel_list[i]
            if not channel.get_busy():
                return channel
    
    def make_sound(self, effect):
        if self.ing:
            channel = self.get_channel()
            if channel != None:
                if effect == "player_bullet":
                    self.player_bullet_effect.set_volume(self.volume)
                    channel.play(self.player_bullet_effect)

                elif effect == "player_jewerly":
                    self.player_jewerly_effect.set_volume(self.volume)
                    channel.play(self.player_jewerly_effect)

                elif effect == "player_upgrade":
                    self.player_upgrade_effect.set_volume(self.volume)
                    channel.play(self.player_upgrade_effect)
                    
                elif effect == "player_explosion":
                    self.player_explosion_effect.set_volume(self.volume)
                    channel.play(self.player_explosion_effect)

                elif effect == "enemy_bullet":
                    self.enemy_bullet_effect.set_volume(self.volume)
                    channel.play(self.enemy_bullet_effect)

                elif effect == "enemy_explosion":
                    self.enemy_explosion_effect.set_volume(self.volume)
                    channel.play(self.enemy_explosion_effect)

                elif effect == "collision":
                    self.collision_effect.set_volume(self.volume)
                    channel.play(self.collision_effect)

                elif effect == "menu_bar":
                    self.menu_bar_effect.set_volume(self.volume)
                    channel.play(self.menu_bar_effect)    

        
import random
import pygame
import math
from enviroment import Enviroment as env

class Util:
    @staticmethod
    def is_probability(percent):
        return random.random() < percent
    
    @staticmethod
    def rotates(image, sprites, angle_inc):
        angle = 0
        for _ in range(360):
            sprites.append(pygame.transform.rotozoom(image, angle, 1))
            angle += angle_inc

    @staticmethod
    def resize_image(image, resize_px):
        width = image.get_width()
        height = image.get_height()
        aspect_ratio = width / height

        target_width = resize_px
        target_height = int(target_width / aspect_ratio)
        return pygame.transform.scale(image, (target_width, target_height))

    @staticmethod
    def set_opacity(surface, opacity):
        temp_surface = surface.copy()
        temp_surface.set_alpha(opacity)
        return temp_surface
    
    @staticmethod
    def transfer_color(image, new_color):
        new_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)    
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                pixel_color = image.get_at((x, y))            
                if pixel_color.a >= 255:
                    new_image.set_at((x, y), new_color)
                else:
                    new_image.set_at((x, y), (0, 0, 0, 0))
        
        return new_image
    
    @staticmethod
    def pos_to_angle(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1        
        angle_radians = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle_radians)        
        # 각도가 음수일 경우 360을 더해줌
        if angle_degrees < 0:
            angle_degrees += 360
        return angle_degrees
    
    @staticmethod
    def load_prperties(file_path):
        properties = {}
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    if ':' in line:  # ':'가 포함된 줄을 속성으로 간주
                        key, value = line.split(':', 1)
                        properties[key.strip()] = value.strip()
        except FileNotFoundError:
            return None
        
        # 결과 출력
        # for key, value in properties.items():
        #     print(f"{key}: {value}")        
        return properties
    
    @staticmethod
    def save_prperties(file_path, properties):
        with open(file_path, 'w') as file:
            for key, value in properties.items():
                file.write(f"{key}: {value}\n")
         
    @staticmethod        
    def print_text(main, txt, x, y, size, color, align, shadow):
        if size == "LARGE":
            text = main.resources.galmuri_font_45.render(txt, True, color)
            text_shadow = main.resources.galmuri_font_45.render(txt, True, env.GRAY)
            margin = 3
        elif size == "MIDDLE":
            text = main.resources.galmuri_font_35.render(txt, True, color)
            text_shadow = main.resources.galmuri_font_35.render(txt, True, env.GRAY)
            margin = 2
        elif size == "MIDDLE2":
            text = main.resources.galmuri_font_30.render(txt, True, color)
            text_shadow = main.resources.galmuri_font_30.render(txt, True, env.GRAY)
            margin = 2
        elif size == "MIDDLE3":
            text = main.resources.galmuri_font_20.render(txt, True, color)
            text_shadow = main.resources.galmuri_font_20.render(txt, True, env.GRAY)
            margin = 2
        else:
            text = main.resources.galmuri_font_15.render(txt, True, color)
            text_shadow = main.resources.galmuri_font_15.render(txt, True, env.GRAY)
            margin = 1
            
        if shadow:
            text_rect = text_shadow.get_rect()
            if align == env.LEFT:
                text_rect.left = x + margin
                text_rect.y = y + margin
            elif align == env.RIGHT:
                text_rect.right = x + margin
                text_rect.y = y + margin
            else:
                text_rect.center = (x + margin, y + margin)
            main.screen.blit(text_shadow, text_rect)
            
        text_rect = text.get_rect()
        if align == env.LEFT:
            text_rect.left = x
            text_rect.y = y
        elif align == env.RIGHT:
            text_rect.right = x
            text_rect.y = y
        else:
            text_rect.center = (x, y)
        main.screen.blit(text, text_rect)
         
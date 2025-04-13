import pygame

class Settings():

    def __init__(self):
        self.screen_height = 640
        self.screen_width = 1280
        self.screen_bgcolor = (230, 230, 230)

        
        self.ship_limit = 3


        self.bullet_height = 15
        self.bullet_width = 3
        self.bullet_color = 60, 60, 60
        
        self.fleet_drop_speed = 10


        self.speedup_scale = 1.1
        self.score_scale = 1.5

        pygame.mixer.init()
        self.bullet_sound = pygame.mixer.Sound('assets/sound/laser.mp3')
        self.bullet_sound.set_volume(0.3)
        self.hit_sound = pygame.mixer.Sound('assets/sound/hit.mp3')
    

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3


        self.alien_speed_factor = 1
        
        self.fleet_direction = 1

        self.alien_points = 50
    

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
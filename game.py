import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():

    ai_settings = Settings()
    
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    pygame.mixer.music.load('assets/sound/bg_music.mp3')
    pygame.mixer.music.play(-1)

    ship = Ship(ai_settings, screen)
    stats = GameStats(ai_settings)
    play_button = Button(screen, "PLAY!")
    sb = Scoreboard(ai_settings, screen, stats)
    bullets = Group()
    aliens = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    while True:

        gf.check_events(ai_settings, stats, play_button, screen, sb, ship, aliens, bullets)

        if stats.game_active:

            ship.update()
            gf.update_bullets(ai_settings, screen, ship, sb, stats, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
        
        gf.update_screen(ai_settings, stats, screen, ship, sb, bullets, aliens, play_button)
    

run_game()



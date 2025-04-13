import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings, stats, play_button, screen, sb, ship, aliens, bullets):
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, stats, screen, sb, ship, aliens, bullets)
        
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets, mouse_x, mouse_y)
                

def check_keydown_events(event, ai_settings, stats, screen, sb, ship, aliens, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        new_bullets = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullets)
        ai_settings.bullet_sound.play()
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        reset(ai_settings, screen, ship, aliens, bullets)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_play_button(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        reset(ai_settings, screen, ship, aliens, bullets)


def reset(ai_settings, screen, ship, aliens, bullets):
    bullets.empty()
    aliens.empty()

    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def create_alien(ai_settings, screen, aliens, num_alien, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * num_alien
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_no_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    no_aliens = int(available_space_x / (2 * alien_width))
    return no_aliens


def get_no_rows(ai_settings, ship_height, alien_height):
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    no_rows = int(available_space_y / (2 * alien_height))
    return no_rows


def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    
    no_aliens = get_no_aliens_x(ai_settings, alien.rect.width)
    no_rows = get_no_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(no_rows):
        for num_alien in range(no_aliens):
            create_alien(ai_settings, screen, aliens, num_alien, row_number)

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def check_bullet_alien_col(ai_settings, screen, ship, sb, stats, aliens, bullets):

    collision = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collision:
        for aliens in collision.values():
            ai_settings.hit_sound.play()
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)


    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):

    if stats.ships_left > 0:
        stats.ships_left -= 1

        sb.prep_ships()

        reset(ai_settings, screen, ship, aliens, bullets)

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)

def update_bullets(ai_settings, screen, ship, sb, stats, aliens, bullets):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_col(ai_settings, screen, ship, sb, stats, aliens, bullets)



def update_screen(ai_settings, stats, screen, ship, sb, bullets, aliens, play_button):
    
    screen.fill(ai_settings.screen_bgcolor)
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from scoreboard import Scoreboard


def check_keydown_events(event,ai_settings,screen,ship,bullets):
      """Respond to Keypresses"""
      if event.key == pygame.K_RIGHT:
            ship.moving_right = True
      elif event.key == pygame.K_LEFT:
            ship.moving_left = True
      elif event.key == pygame.K_SPACE:
            fire_bullet(ai_settings,screen,ship,bullets)

def check_keyup_events(event,ship):
      """Respond to Key releases"""
      if event.key == pygame.K_RIGHT:
            ship.moving_right = False
      elif event.key == pygame.K_LEFT:
            ship.moving_left = False     

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
                score_file = open("HighScore.txt", "a")
                score_file.write(str(stats.high_score))
                pygame.quit()
                sys.exit()
      elif event.type == pygame.KEYDOWN:
              check_keydown_events(event,ai_settings,screen,ship,bullets) 
      elif event.type == pygame.KEYUP:
              check_keyup_events(event,ship)
      elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
      button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
      if button_clicked and not stats.game_active:
            #reset the game settings.
            ai_settings.initialize_dynamic_settings()
            #Hide the mouse cursor.
            pygame.mouse.set_visible(False )
            stats.reset_stats()
            stats.game_active = True
            # Reset the scoreboard images.
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()

            aliens.empty()
            bullets.empty()

            create_fleet(ai_settings,screen,ship,aliens)
            ship.center_ship()

def fire_bullet(ai_settings,screen,ship,bullets):
      if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings , screen,ship)
            bullets.add(new_bullet)      

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    """Updates images on the screen and flip to the new screen"""
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
          bullet.draw_bullet()     
    ship.blitme() 
    aliens.draw(screen)
    # Draw the score information
    sb.show_score()
    if not stats.game_active:
          play_button.draw_button()     
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
      """Update position of bullets and get rid of old bullets."""
      bullets.update()
      for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
      print(len(bullets)) 
      check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):      
      """Respond to bullet-alien collisions."""
      # Remove any bullets and aliens that have collided
      collisions = pygame.sprite.groupcollide(aliens,bullets,True ,True)
      if collisions:
          for aliens in collisions.values():  
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
      check_high_score(stats,sb)      
      if len(aliens)== 0:
            # If the entire fleet is destroyed, start a new level.
            # Destroy existing bullets,speed up game and create new fleet.
            bullets.empty()
            ai_settings.increase_speed()
            # Increase level.
            stats.level += 1
            sb.prep_level()
            create_fleet(ai_settings,screen,ship,aliens)

def get_number_alien(ai_settings,alien_width):
      available_space_x = ai_settings.screen_width - 3 * alien_width
      number_aliens_x = int(available_space_x / (2 * alien_width ))
      return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
      """Determine the number of rows of aliens that fit on the screen."""
      available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
      number_rows = int(available_space_y / (2 * alien_height))
      return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
      alien = Alien(ai_settings,screen)
      alien_width = alien.rect.width
      alien.x = alien_width + 2 * alien_width * alien_number
      alien.rect.x = alien.x
      alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
      aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
        """Create a full fleet of aliens."""
        alien = Alien(ai_settings,screen)
        number_aliens_x = get_number_alien(ai_settings,alien.rect.width)
        number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
        #create the first row of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                  create_alien(ai_settings,screen,aliens,alien_number,row_number)
                  
def check_fleet_edges(ai_settings,aliens):
      """Respond appropriately if any aliens have reached an edge."""
      for alien in aliens.sprites():
            if alien.check_edges():
                  change_fleet_direction(ai_settings,aliens)
                  break

def change_fleet_direction(ai_settings,aliens):
      for alien in aliens.sprites():
            alien.rect.y += ai_settings.fleet_drop_speed
      ai_settings.fleet_direction *= -1                                    

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
      """Update the postions of all aliens in the fleet."""
      check_fleet_edges(ai_settings ,aliens)
      aliens.update()
      #look for alien-ship collisions.
      if pygame.sprite.spritecollideany(ship ,aliens):
            ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
      check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets)

def ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets):
      """Respond to ship being hit by alien."""
      if stats.ships_left > 0:
            #Decrement ships_left.
            stats.ships_left -= 1

            # Update  scoreboard.
            sb.prep_ships()
            #empty the list of aliens and bullets
            aliens.empty()
            bullets.empty()
            create_fleet(ai_settings,screen,ship,aliens)
            ship.center_ship()
            #pause
            sleep(0.5)
      else:
            stats.game_active = False
            pygame.mouse.get_visible      

def check_aliens_bottom(ai_settings,screen,stats,sb,ship,aliens,bullets):
      """Check if any aliens have reached the bottom of the screen."""
      screen_rect = screen.get_rect()
      for alien in aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                  ship_hit(ai_settings,screen,stats,sb,ship,aliens,bullets)
                  break

def check_high_score(stats,sb):
      """Check to see if theres a new high score. """
      if stats.score > stats.high_score:
            stats.high_score = stats.score
            sb.prep_high_score()
import sys,pygame
from bullets import Bullet
from alien import Alien
from time import sleep
from ship import Ship
from game_stats import GameStats as gs


'''This portion is responsible for the aliens'''

def create_fleet(game_settings,screen,ship,aliens):
    '''create a fleet of aliens'''
    #creating an alien and getting the number of aliens in a row
    #spacing between each alien is equal to one alien width
    alien=Alien(game_settings,screen)
    number_aliens_x=get_number_aliens_x(game_settings,alien.rect.width)
    number_rows=get_number_rows(game_settings,ship.rect.height,alien.rect.height)

    #Creating the first row now
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings,screen,aliens,alien_number,row_number)


def create_alien(game_settings,screen,aliens,alien_number,row_number):
    #Creating an alien and placing in a row
    alien=Alien(game_settings,screen)
    alien_width=alien.rect.width
    alien.x=alien_width + 2 * alien_width * alien_number
    alien.rect.x=alien.x
    alien.rect.y=alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(game_settings,ship_height,alien_height):
    '''determine the no. of rows of aliens to fit on the screen'''
    available_space_y=(game_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows=int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens_x(game_settings,alien_width):
    '''Determine the number of aliens that fit in a row'''
    available_space_x=game_settings.screen_width - 2 * alien_width
    number_aliens_x=int(available_space_x / (2 * alien_width))
    return number_aliens_x


def update_aliens(game_settings,screen,stats,sb,ship,aliens,bullets):
    '''checking to see if edge reached and Updating the aliens position on the screen'''
    check_fleet_edges(game_settings,aliens)
    aliens.update()
    #look for alien-ship collision
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(game_settings,screen,stats,sb,ship,aliens,bullets)
    #Look for aliens reaching the bottom of the screen
    check_aliens_bottom(game_settings,screen,stats,sb,ship,aliens,bullets)

def check_fleet_edges(game_settings,aliens):
    '''respond if alien reaches edge'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings,aliens)
            break


def change_fleet_direction(game_settings,aliens):
    '''Dropping and changing fleet direction'''
    for alien in aliens.sprites():
        alien.rect.y+=game_settings.fleet_drop_speed
    game_settings.fleet_direction*=-1

def check_aliens_bottom(game_settings,screen,stats,sb,ship,aliens,bullets):
    '''checking to see if aliens have reached the bottom of the screen'''
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #treating the same was as when ship is hit
            ship_hit(game_settings,screen,stats,sb,ship,aliens,bullets)
            break

'''End alien'''




'''This part is responsible for the bullets'''

def fire_bullet(game_settings,screen,ship,bullets):
    '''Fire a bullet if limit not reached'''
    #create a new bullet and add it to the group
    if len(bullets) < game_settings.bullet_allowed:
        new_bullet=Bullet(game_settings,screen,ship)
        bullets.add(new_bullet)


def update_bullets(game_settings,screen,stats,sb,ship,aliens,bullets):
    bullets.update()
    #Deleting old bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <=0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(game_settings,screen,stats,sb,ship,aliens,bullets)


def check_bullet_alien_collisions(game_settings,screen,stats,sb,ship,aliens,bullets):
     # checking to see if bullet hit alien, then removing both bullet and alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
             stats.score+=game_settings.alien_points*len(aliens)
             sb.prep_score()
        check_high_scores(stats,sb)
    if len(aliens) == 0:
        #If the entire fleet is destroyed, start a new level
        # Destroy existing bullet and spawn a new fleet ad speed up the fucking game
        bullets.empty()
        game_settings.increase_speed()
        #Increase level
        stats.level+=1
        sb.prep_level()
        create_fleet(game_settings, screen, ship, aliens)

'''End bullets'''





'''This part is responsible for the ship'''

def ship_hit(game_settings,screen,stats,sb,ship,aliens,bullets):
    '''respond to ship being hit by alien'''
    if stats.ships_left > 1:
        #Decrement ships left
        stats.ships_left-=1

        #Update scoreboard
        sb.prep_ships()

        #Empty list of aliens & bullets
        aliens.empty()
        bullets.empty()

        #Creating new fleet and center the ship
        create_fleet(game_settings,screen,ship,aliens)
        ship.center_ship()

        #Pause
        sleep(0.5)

    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)

'''End ship'''






'''This part is the event checker'''

def check_keydown_events(event,game_settings,screen,ship,bullets):
    '''respond to keypresses'''
    # move the ship right and left
    if event.key==pygame.K_RIGHT:
        ship.moving_right=True
    elif event.key==pygame.K_LEFT:
        ship.moving_left=True
    elif event.key==pygame.K_q:
        sys.exit()
    #Moving the ship up & down
    elif event.key==pygame.K_UP:
        ship.moving_up=True
    elif event.key==pygame.K_DOWN:
        ship.moving_down=True
    #firing the bullets
    elif event.key==pygame.K_SPACE:
        fire_bullet(game_settings,screen,ship,bullets)


def check_keyup_events(event,ship):
    '''respond to key releases'''
    if event.key==pygame.K_RIGHT:
        ship.moving_right=False
    elif event.key==pygame.K_LEFT:
        ship.moving_left=False
    elif event.key==pygame.K_UP:
        ship.moving_up=False
    elif event.key==pygame.K_DOWN:
        ship.moving_down=False


def check_events(game_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    '''Follow keyboard & mouse events'''
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,game_settings,screen,ship,bullets)
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(game_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)


def check_play_button(game_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    '''start a new game when player hits play'''
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        ship.center_ship()
        game_settings.initialize_dynamic_settings()
        #hide the mouse cursor
        pygame.mouse.set_visible(False)
         #Reset the game stats
        stats.reset_stats()
        stats.game_active=True

        #Reset the scoreboard images
        sb.prep_level()
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_ships()

        #Empty the list of bullets and aliens
        aliens.empty()
        bullets.empty()

         #Create new fleet and center the ship
        create_fleet(game_settings,screen,ship,aliens)
        # ship.center_ship()


def update_screen(game_settings,screen,stats,sb,ship,aliens,bullets,background,play_button):
    '''updating images on the screen and flipping to new one'''
    #Filling colors at each pass
    # screen.fill(game_settings.bg_color)
    screen.blit(background,(0,0))
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    ship.blitme()
    #Update the game screen
    pygame.display.flip()


def check_high_scores(stats,sb):
    '''Check to see if there is a new high score'''
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()


'''End checking events'''

import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    #Initializes the game and sets the screen
    pygame.init()
    game_settings=Settings()
    screen=pygame.display.set_mode((game_settings.screen_width,game_settings.screen_height))
    pygame.display.set_caption('Alien Shooter')

    #Creating instance to store game statistics
    stats=GameStats(game_settings)

    #making a ship
    ship=Ship(game_settings,screen)

    #make a group to store bullets
    bullets=Group()

    #Making a alien
    aliens=Group()

    # #Make a star
    background=pygame.image.load('images/star.jpeg')


    #Creating feelt of aliens
    gf.create_fleet(game_settings,screen,ship,aliens)

    #Make the play button
    play_button=Button(game_settings,screen,'Play')

    #Create instance to store score and stats
    sb=Scoreboard(game_settings,screen,stats)

    #Starting the game loop
    while True:
        gf.check_events(game_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            # ship.update()
            gf.update_bullets(game_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(game_settings,screen,stats,sb,ship,aliens,bullets)
            ship.update()
        gf.update_screen(game_settings,screen,stats,sb,ship,aliens,bullets,background,play_button)




run_game()

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,game_settings,screen):
        '''set the starting position of player ship'''
        super().__init__()
        self.screen=screen
        self.game_settings=game_settings

        #Loading ths ship image
        self.image=pygame.image.load('images/player_ship.jpg')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()

        #Starting the ship at the bottom of the screen and defining the x & y coordinates
        self.rect.centerx=self.screen_rect.centerx
        self.rect.centery=self.screen_rect.centery
        self.rect.bottom=self.screen_rect.bottom

        #Storing decimal value for smooth movement although centerx only takes integer
        self.side=float(self.rect.centerx)
        self.updown=float(self.rect.centery)

        #Movement flags to control the ship
        self.moving_right=False
        self.moving_left=False
        self.moving_up=False
        self.moving_down=False
        # self.center_ship()

    def update(self):
        '''updating the ship's position based on the movement flag'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.side+=self.game_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.side-=self.game_settings.ship_speed_factor

        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.updown-=self.game_settings.ship_speed_factor

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.updown+=self.game_settings.ship_speed_factor

        #Updating the rect object from self.center
        self.rect.centerx=self.side
        self.rect.centery=self.updown

    def center_ship(self):
        '''center the ship on the screen'''
        self.centerx=self.screen_rect.centerx


    def blitme(self):
        '''drawing the ship at it's current location'''
        self.screen.blit(self.image, self.rect)

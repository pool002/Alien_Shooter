import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    '''class to represent a single alien'''
    def __init__(self,game_settings,screen):
        '''Initialize the alien and its starting pos'''
        super().__init__()
        self.screen=screen
        self.game_settings=game_settings

        #Loading the alien image and getting rect
        self.image=pygame.image.load('images/alien.jpg')
        self.rect=self.image.get_rect()

        #Start each new alien on top and left side of the screen
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height

        #Storing the alien's pos
        self.x=float(self.rect.x)

    def blitme(self):
        '''drawing the alien at it's current position'''
        self.screen.blit(self.image,self.rect)

    def update(self):
        '''Moving the alien right' or left'''
        self.x+=(self.game_settings.alien_speed_factor * self.game_settings.fleet_direction)
        self.rect.x=self.x



    def check_edges(self):
        '''returns true if aliens has hit the edge of the screen'''
        screen_rect=self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
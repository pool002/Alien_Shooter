import pygame
from pygame.sprite import Sprite as spr

class Bullet(spr):
    '''a class to manage bullets fired from the  ship'''

    def __init__(self,game_settings,screen,ship):
        '''create a bullet object at the ship's position'''
        super().__init__()
        self.screen=screen

        #Creating bullet rect at (0,0) then matching with ship
        self.rect=pygame.Rect(0,0,game_settings.bullet_width,game_settings.bullet_height)
        self.rect.centerx=ship.rect.centerx
        self.rect.top=ship.rect.top

        #Storing the bullet position as a decimal value
        self.y=float(self.rect.y)

        self.color=game_settings.bullet_color
        self.speed_factor=game_settings.bullet_speed_factor



    def update(self):
        '''Moving the bullet up the screen'''
        #Here we use the decimal value to change the position
        self.y-=self.speed_factor
        #updating the rect position
        self.rect.y=self.y


    def draw_bullet(self):
        '''draw bullet to the screen'''
        pygame.draw.rect(self.screen,self.color,self.rect)

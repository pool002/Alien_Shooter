#Settings file
class Settings():
    '''settings for alien shooter'''
    def __init__(self):
        '''initialize the game 's static settings'''
        self.screen_width=1920
        self.screen_height=1080
        self.bg_color=(0,0,0)

        #Ship settings
        self.ship_speed_factor=4
        self.ship_limit=3

        #Bullet settings
        self.bullet_speed_factor=3
        self.bullet_width=10
        self.bullet_height=16
        self.bullet_color=(255,255,255)
        self.bullet_allowed=5

        #Alien settings
        self.alien_speed_factor=5
        self.fleet_drop_speed=10


        #how quiqkly the game speeds up
        self.speedup_scale=1.1

        #how quiqkly the alien point values increase
        self.score_scale=1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Initialize the settings that change throughout the game'''
        self.ship_speed_factor=4.5
        self.bullet_speed_factor=4
        self.alien_speed_factor=3.5
        # fleet direction of 1 goes right ;  -1 goes left
        self.fleet_direction = 1

        #Scoring
        self.alien_points=50

    def increase_speed(self):
        '''Increase the speed settings' and alien point values'''
        self.ship_speed_factor*=self.speedup_scale
        self.bullet_speed_factor*=self.speedup_scale
        self.alien_speed_factor*=self.speedup_scale
        self.alien_points=int(self.alien_points*self.score_scale)

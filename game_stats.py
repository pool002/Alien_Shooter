class GameStats():
    '''Track statsitics for ai'''
    def __init__(self,game_settings):
        '''initialize the stats'''
        #Starting ai in an inactive state
        self.game_active=False
        self.game_settings=game_settings
        self.reset_stats()
        #high score should never be reset
        self.high_score=0

    def reset_stats(self):
        '''stats that can change during the game'''
        self.ships_left=self.game_settings.ship_limit
        self.score=0
        self.level=1
class Settings():
    """A Class to store All  settings  for alien Invasion."""
    
    def __init__(self):      #Automatically call when we call the class.
        """initialize the game settings"""
        self.screen_width = 1360
        self.screen_height = 720
        self.bg_color = (0,0,0)
        self.ship_speed_factor = 1
        # Ship settings
        self.ship_limit = 3
        # Bullet settings
        self.bullet_speed_factor = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 0,0,155
        self.bullets_allowed = 5
        # Alien speed setting
        self.alien_speed_factor = 0.5
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        # How quickly the game speeds up
        self.speedup_scale = 1.1
        # How quickly the aliens point values increase 
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 3
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 2
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        #scoring 
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale 
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)   
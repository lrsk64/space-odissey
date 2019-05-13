class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""
    def __init__(self):
        """Инициализирует настройки игры."""
        # Параметры экрана
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (30, 30, 30)

        # Параметры пули
        self.bullet_width = 6
        self.bullet_height = 23
        self.bullets_allowed = 3

        # Параметры корабля
        self.ship_limit = 3

        #Параметры метеорита
        self.meteor_width = 60
        self.meteor_height = 53
        self.meteors_allowed = 1

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

        self.collisions_count = 0

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 3
        self.bullet_speed_factor = 2
        self.meteor_speed_factor = 1
        self.meteor_points = 50

    def increase_speed_points(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.meteor_speed_factor *= self.speedup_scale
        self.meteor_points = int (self.meteor_points * self.score_scale)
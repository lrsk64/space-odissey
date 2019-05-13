import pygame
import random
from pygame.sprite import Sprite
import spritesheet
from settings import Settings

class Meteor(Sprite):
    """Класс для управления метеоритами"""
    def __init__(self, screen):
        settings = Settings()
        super().__init__()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.image.load('images/meteor.png')
        self.rect = self.image.get_rect()

        # Создание пули в позиции (0,0) и назначение правильной позиции.
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(settings.screen_width - settings.meteor_width)
        self.rect.y = 5

        # Позиция метеорита хранится в вещественном формате.
        self.y = float(self.rect.y)
        self.speed_factor = settings.meteor_speed_factor

    def update(self):
        """Перемещает метеорит вниз по экрану."""
        # Обновление позиции пули в вещественном формате.
        self.y += self.speed_factor
        self.rect.y = self.y

    def draw_meteor(self):
        """Вывод метеориты на экран."""
        self.screen.blit(self.image, self.rect)

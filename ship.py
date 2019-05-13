import pygame
from settings import Settings
from pygame.sprite import Sprite



class Ship(Sprite):
    def __init__(self, settings, screen):
        """Инициализирует корабль и задает его начальную позицию."""
        super().__init__()
        self.screen = screen
        self.settings = Settings()
        # Загрузка изображения корабля и получение прямоугольника.
        self.image = pygame.image.load('images/ship.png')
        self.change_image = self.image
        self.image_hit = pygame.image.load('images/explosion.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Каждый новый корабль появляется у нижнего края экрана.
        self.center_ship()

        # Флаги перемещения
        self.moving_right = False
        self.moving_left = False

    def update(self, settings):
        """Обновляет позицию корабля с учетом флага"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= settings.ship_speed_factor

    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom